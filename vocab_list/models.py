import csv
import json
import unicodedata

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from django_rq import job
from iso639 import languages

from lemmatization.models import FormToLemma, Lemma
from lemmatized_text.models import LemmatizedText


def strip_diacritics(s):
    return unicodedata.normalize(
        "NFC",
        "".join((
            c
            for c in unicodedata.normalize("NFD", s)
            if unicodedata.category(c) != "Mn"
        ))
    )


# TODO: Investigate using this decorator within the class
@job("default", timeout=600)
def link_vl_node(model, pk):
    obj = model.objects.get(pk=pk)
    obj.link()


def validate_lines(lines: list, entry_model: models.Model) -> list:
    """
    Make sure that the provided lines are unique, and that they have only the
    metadata fields that are valid for the given `entry_model`.

    Args:
        lines: A list of dicts representing new vocabulary entries to be added.
            The dicts are expected to be in {fieldName: value} format, as this
            function will compare those field names with a list of field names
            from the model and remove any pairs where the key is not a valid
            field name.
        entry_model: The model for the vocabulary list entry that will be used.
            This should inherit from `AbstractVocabListEntry`
    """
    # Remove any empty values from lines dicts
    lines = [{k: v for k, v in line.items() if v} for line in lines]

    # Make sure that lines aren't repeated,
    # method described in https://stackoverflow.com/a/11092607
    unique_line_strings = set([json.dumps(line, sort_keys=True) for line in lines])
    unique_lines = [json.loads(linestring) for linestring in unique_line_strings]
    if len(unique_lines) == 0:
        # As far as I can tell, there's no proper logging in the project, but there probably should be
        print(f"No unique lines found in lines: {list(lines)}")
        return []

    # lowercase all the keys on the unique lines
    for i, line in enumerate(unique_lines):
        unique_lines[i] = {k.lower(): v for k, v in line.items()}

    # get the fields that exist in the model
    model_fields = [f.name for f in entry_model._meta.get_fields()]
    # check for foreign key fields and add "_id" to the end of the field name
    for i, field in enumerate(model_fields):
        fieldType = entry_model._meta.get_field(field).get_internal_type()
        if fieldType == "ForeignKey":
            model_fields[i] = model_fields[i] + "_id"

    # valid fields are the ones that exist in the uploaded data
    # since we're using dictreader, all lines should have the same keys,
    # so we only need to check against the first one.
    valid_fields = list(filter(lambda x: x in unique_lines[0], model_fields))

    # Filtering each line down to a dict that just has the fields in valid fields
    # meaning it won't try to add data to fields that don't exist or that it can't add to
    for i, line in enumerate(unique_lines):
        unique_lines[i] = {fieldname: line[fieldname] for fieldname in valid_fields if fieldname in line}

    return unique_lines


def find_lemma(headword):
    headword_no_macrons = strip_diacritics(headword)
    lemma_matches = Lemma.objects.filter(lemma=headword_no_macrons).order_by("rank").first()
    if lemma_matches:
        return lemma_matches
    if not lemma_matches:
        lemma_matches = Lemma.objects.filter(lemma=headword).order_by("rank").first()
        if not lemma_matches:
            formtolemma_matches = FormToLemma.objects.filter(form=headword).first()
            try:
                lemma_id = formtolemma_matches.lemma_id
                lemma_matches = Lemma.objects.get(id=lemma_id)
            except AttributeError:
                return None
    return lemma_matches


class AbstractVocabList(models.Model):
    """
    An abstract vocabulary list entry class.

    Entries should have a **headword** and **gloss** (definition), and are expected
    to be linked into the lattice.

    Note that a headword may be repeated in a list if it has different definitions. For example,
    the latin word quam may be included three times:

        quam - as possible as
        quam - how
        quam - than
    """
    lang = models.CharField(max_length=3)  # ISO 639.2
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def display_name(self):
        """
        Returns the display name of self.lang
        """
        return languages.get(part3=self.lang).name

    def _create_entries(self, lines: csv.DictReader, entry_model: models.Model, familiarity: int = 0) -> list:
        """
        Creates vocab list entries from provided lines.

        New vocab list entries are created with the provided model, since there
        are different models for personal vocab lists and regular vocab lists.
        Ensures that new entries are not duplicates with the `get_or_create()`
        function off of `entry_model.objects`.

        Args:
            lines: List of dicts corresponding to entries to be created. This
                function assumes that the dict keys have already been
                validated, so that they should only contain values that can be
                added to the provided data model.
            entry_model: Django model that the vocab list entries should be
                created as. The model should inherit from
                `AbstractVocabListEntry`
            familiarity: A familiarity score to use as a default if none is
                provided. Defaults to zero, in which case familiarity scores
                won't be taken into account.
        """
        # If using familiarity scores, set a default value on each line if
        # familiarity is not set.
        if familiarity > 0:
            for line in lines:
                if "familiarity" in line:
                    line["familiarity"] = line["familiarity"] or familiarity
                else:
                    line["familiarity"] = familiarity

        # Get or create the entries
        entries = [entry_model.objects.get_or_create(
            vocabulary_list=self,
            defaults={
                "_order": 1
            },
            **line
        )[0] for line in lines]
        return entries

    def load_tab_delimited(self, fd, entry_model: models.Model, familiarity: int = 0, **kwargs):
        """
        Method to load vocab lists from tsv upload.
        Parameters: fd (iterable), entry_model (class), extra_attrs (dict)
        Returns: bulk create query of vocab list entries
        """
        decoded_file = fd.read().decode("utf-8").splitlines()
        lines = csv.DictReader(decoded_file, delimiter="\t")

        valid_lines = validate_lines(lines, entry_model)

        entries = self._create_entries(valid_lines, entry_model, familiarity=familiarity)
        return entries


class VocabularyList(AbstractVocabList):

    # a NULL owner means a system-provided vocabulary list
    owner = models.ForeignKey(
        getattr(settings, "AUTH_USER_MODEL", "auth.User"),
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    cloned_from = models.ForeignKey(
        "self", null=True, editable=False, on_delete=models.SET_NULL
    )

    def load_tab_delimited(self, fd):
        return super().load_tab_delimited(fd, VocabularyListEntry)

    @property
    def link_status(self):
        return self.entries.filter(link_job_ended__isnull=False).count() / self.entries.count()

    class Meta:
        verbose_name = "vocabulary list"

    def __str__(self):
        return self.title

    def data(self):
        return {
            "id": self.pk,
            "title": self.title,
            "description": self.description,
            "link_status": self.link_status,
            "owner": self.owner.email if self.owner else None,
        }


class PersonalVocabularyList(AbstractVocabList):
    # TODO: this could be refacted to the abstract class, but VocabularyList defines it as "owner"
    user = models.ForeignKey(
        getattr(settings, "AUTH_USER_MODEL", "auth.User"),
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "personal vocabulary list"
        unique_together = [("user", "lang")]

    def __str__(self):
        return f"{self.user} personal {self.lang} vocab list"

    def node_familiarity(self):
        return 10

    def load_tab_delimited(self, fd, familiarity):
        return super().load_tab_delimited(fd, PersonalVocabularyListEntry, familiarity=familiarity)

    def data(self):
        stats = {}
        for stat in self.personalvocabularystats_set.all():
            stats[stat.text.pk] = stat.data()
        return {
            "entries": [w.data() for w in self.entries.all().order_by("headword")],
            "statsByText": stats,
            "id": self.pk
        }


class AbstractVocabListEntry(models.Model):
    """
    Base class for vocab list entries.

    Vocab list entries are matched against lemma used in texts to determine if
    a word is known. This base class defines the core elements of the entries
    and provides functionality to link those entries to their lemma via an
    async job.

    Args:
        headword: Dictionary definition for vocab list entry, expected to look
            something like "sum, esse, fui, futurus". The first word of the
            headword will be used to match a lemma in the database.
        lemma: Foreign key to link to the lemma in the database
        definition: User-supplied definition for the term, not connected to the
            gloss for the related lemma.
        link_job_id:
        link_job_started:
        link_job_ended:

    TODO: Add vue components for matching headword lemma
    """
    headword = models.CharField(max_length=255)
    lemma = models.ForeignKey(Lemma, null=True, on_delete=models.SET_NULL)
    definition = models.TextField(blank=True)
    link_job_id = models.CharField(max_length=250, blank=True)
    link_job_started = models.DateTimeField(null=True)
    link_job_ended = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def link(self):
        """
        Links a headword as entered to a lemma in the database.

        This function looks for an exact match to the headword provided, and
        links the entry to the lowest-ranked lemma entry (e.g. rank 1 is
        preferred to rank 10). This function runs as a job via the `link_job`
        function on this object and `link_vl_node` declared in this file.
        """
        headword = self.headword.split()[0].strip(",")
        lemma_matches = find_lemma(headword)
        if lemma_matches:
            # Use the lowest-ranked lemma whether or not there are multiple matches
            lemma = lemma_matches
            self.lemma = lemma
            self.link_job_ended = timezone.now()
            self.save()
        else:
            # There are no lemma matches, don't save a linked lemma
            self.link_job = timezone.now()
            self.save()

    def link_job(self):
        """
        Call the `link_vl_node` async function passing `self.__class__` as the
        model so that the `link()` function can be run as a job.
        """
        if not self.lemma:
            j = link_vl_node.delay(self.__class__, self.pk)
            self.link_job_id = j.id
            self.link_job_started = timezone.now()
            self.save()

    def data(self, **kwargs):
        return {
            "id": self.pk,
            "headword": self.headword,
            "definition": self.definition,
            **kwargs
        }

    def save(self, *args, **kwargs):
        """
        Override default save behavior to run `link_job()` when creating a new
        instance of a vocabulary list entry. When the entry is new, there is no
        pk, so save the instance first then run the `link_job`
        """
        if not self.pk:
            super().save(*args, **kwargs)
            self.link_job()
        else:
            super().save(*args, **kwargs)


class VocabularyListEntry(AbstractVocabListEntry):
    """
    Vocabulary list entries for re-usable vocabulary lists.

    Vocab list entries are matched against lemma used in texts to determine if
    a word is known. This inherits from `AbstractVocabListEntry` for
    functionality and adds a link to the parent vocabulary list.

    Args:
        headword: Dictionary definition for vocab list entry, expected to look
            something like "sum, esse, fui, futurus". The first word of the
            headword will be used to match a lemma in the database.
        lemma: Foreign key to link to the lemma in the database
        definition: User-supplied definition for the term, not connected to the
            gloss for the related lemma.
        link_job_id:
        link_job_started:
        link_job_ended:
        vocabulary_list: Foreign key for parent vocabulary list
    """
    vocabulary_list = models.ForeignKey(
        VocabularyList, related_name="entries", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "vocabulary list entry"
        verbose_name_plural = "vocabulary list entries"
        order_with_respect_to = "vocabulary_list"

    def data(self):
        return super().data(lemma=self.lemma_id)


class PersonalVocabularyListEntry(AbstractVocabListEntry):
    """
    Vocabulary list entries for user-specific personal vocabulary lists.

    Personal vocab list entries are matched against lemma used in texts to
    determine if a word is known. This inherits from `AbstractVocabListEntry`
    for functionality and adds a link to the parent personal vocabulary list.
    It also adds a `familiarity` attribute to each entry, which is used to
    indicate how much of a text is well-known.

    Args:
        headword: Dictionary definition for vocab list entry, expected to look
            something like "sum, esse, fui, futurus". The first word of the
            headword will be used to match a lemma in the database.
        lemma: Foreign key to link to the lemma in the database
        definition: User-supplied definition for the term, not connected to the
            gloss for the related lemma.
        link_job_id:
        link_job_started:
        link_job_ended:
        vocabulary_list: Foreign key for parent personal vocabulary list
        familiarity: Number from 1 to 5 representing familiarity with the term.
            1 = I don't recognise this word
            2 = I recognise this word but don't know what it means
            3 = I think I know what this word means
            4 = I definitely know what this word means but could forget soon
            5 = I know this word so well, I am unlikely to ever forget it
    """
    vocabulary_list = models.ForeignKey(
        PersonalVocabularyList, related_name="entries", on_delete=models.CASCADE)
    familiarity = models.IntegerField(
        null=True,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )

    class Meta:
        verbose_name = "personal vocabulary list entry"
        verbose_name_plural = "personal vocabulary list entries"
        order_with_respect_to = "vocabulary_list"

    def data(self):
        return super().data(familiarity=self.familiarity, lemma_id=self.lemma_id, lemma=self.lemma.lemma if self.lemma else self.headword)

    def familiarity_range(self):
        """hack for template iteration"""
        return range(self.familiarity)


# Perhaps these belong in a seperate app - Vocab Stats or something as it
# introduces bringing in dependency on LemmatizedText

class PersonalVocabularyStats(models.Model):
    text = models.ForeignKey(LemmatizedText, on_delete=models.CASCADE)
    vocab_list = models.ForeignKey(PersonalVocabularyList, on_delete=models.CASCADE)

    unranked = models.DecimalField(max_digits=5, decimal_places=4, default="0")
    one = models.DecimalField(max_digits=5, decimal_places=4, default="0")
    two = models.DecimalField(max_digits=5, decimal_places=4, default="0")
    three = models.DecimalField(max_digits=5, decimal_places=4, default="0")
    four = models.DecimalField(max_digits=5, decimal_places=4, default="0")
    five = models.DecimalField(max_digits=5, decimal_places=4, default="0")

    def update(self):
        unique_lemmas = list(set([token["lemma_id"] for token in self.text.data if token["lemma_id"] is not None]))
        ranked_lemmas = [e.lemma_id for e in self.vocab_list.entries.filter(lemma_id__isnull=False)]
        unranked_lemmas = list(filter(lambda lemma_id: lemma_id not in ranked_lemmas, unique_lemmas))
        familiarities = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
        for entry in self.vocab_list.entries.filter(familiarity__isnull=False, lemma__pk__in=unique_lemmas):
            familiarities[str(entry.familiarity)] += 1
        self.unranked = len(unranked_lemmas) / len(unique_lemmas)
        self.one = familiarities["1"] / len(unique_lemmas)
        self.two = familiarities["2"] / len(unique_lemmas)
        self.three = familiarities["3"] / len(unique_lemmas)
        self.four = familiarities["4"] / len(unique_lemmas)
        self.five = familiarities["5"] / len(unique_lemmas)

        self.save()

    def data(self):
        return dict(
            text=self.text.pk,
            personalVocabList=self.vocab_list.pk,
            unranked=self.unranked,
            one=self.one,
            two=self.two,
            three=self.three,
            four=self.four,
            five=self.five,
        )
