import unicodedata

from django.conf import settings
from django.db import models
from django.utils import timezone

from django_rq import job
from iso639 import languages

from lattices.models import LatticeNode, LemmaNode
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


@job("default", timeout=600)
def link_vl_node(model, pk):
    obj = model.objects.get(pk=pk)
    obj.link()


def clean(headword, gloss):
    """Expect a headword and gloss, i.e., two columns,
    & additional columns will be ingnored."""
    return (headword.strip().strip('"'), gloss.strip().strip('"'))


def parse_line(idx, line):
    try:
        columns = line.decode("utf-8").strip().split("\t")
    except UnicodeDecodeError:
        return ("Line " + str(idx), "Bad Data")
    return clean(*columns)


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

    def _create_entires(self, new_headwords, entry_model, extra_attrs):
        """
        Parameters: new_headwords (list), entry_model (class), extra_attrs (dict)
        Returns: list of vocab list entry objects
        """
        return [
            entry_model(vocabulary_list=self, _order=idx, headword=line[0], gloss=line[1], **extra_attrs)
            for idx, line in enumerate(new_headwords)
        ]

    def load_tab_delimited(self, fd, entry_model, extra_attrs={}):
        """
        Method to load vocab lists from tsv upload.
        Parameters: fd (iterable), entry_model (class), extra_attrs (dict)
        Returns: bulk create query of vocab list entries
        """
        lines = [parse_line(idx, line) for idx, line in enumerate(fd)]
        # filter out duplicates in the files
        # how do we know its not a real duplicate vs word duplicate with different definitions? sets!
        filter_repeats_lines = list(set(lines))
        existing_headwords = entry_model.objects.filter(vocabulary_list=self).values_list("headword", "gloss")
        # Must do check for matching headword + definition
        new_headwords = filter(lambda x: x != "" and x not in existing_headwords, filter_repeats_lines)
        entries = self._create_entires(new_headwords, entry_model, extra_attrs)
        return entry_model.objects.bulk_create(entries)


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
        return super().load_tab_delimited(fd, PersonalVocabularyListEntry, extra_attrs={"familiarity": familiarity})

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
    headword = models.CharField(max_length=255)
    gloss = models.TextField(blank=True)
    link_job_id = models.CharField(max_length=250, blank=True)
    link_job_started = models.DateTimeField(null=True)
    link_job_ended = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def link(self):
        first = strip_diacritics(self.headword.split()[0].strip(","))
        lemma_node = LemmaNode.objects.filter(lemma=first).first()
        if lemma_node is None:
            for lemma_node in LemmaNode.objects.filter(lemma__istartswith=first):
                if lemma_node.node.children.exists():
                    break
        if lemma_node:
            self.node = lemma_node.node
        self.link_job_ended = timezone.now()
        self.save()

    def link_job(self, model):
        j = link_vl_node.delay(model, self.pk)
        self.link_job_id = j.id
        self.link_job_started = timezone.now()
        self.save()

    def data(self, **kwargs):
        return {
            "id": self.pk,
            "headword": self.headword,
            "gloss": self.gloss,
            **kwargs
        }


class VocabularyListEntry(AbstractVocabListEntry):
    vocabulary_list = models.ForeignKey(
        VocabularyList, related_name="entries", on_delete=models.CASCADE)
    node = models.ForeignKey(
        LatticeNode, related_name="vocabulary_entries", null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "vocabulary list entry"
        verbose_name_plural = "vocabulary list entries"
        order_with_respect_to = "vocabulary_list"

    def link_job(self):
        return super().link_job(VocabularyListEntry)

    def data(self):
        return super().data(node=self.node_id)


class PersonalVocabularyListEntry(AbstractVocabListEntry):
    vocabulary_list = models.ForeignKey(
        PersonalVocabularyList, related_name="entries", on_delete=models.CASCADE)
    familiarity = models.IntegerField(null=True)
    # 1. I don't recognise this word
    # 2. I recognise this word but don't know what it means
    # 3. I think I know what this word means
    # 4. I definitely know what this word means but could forget soon
    # 5. I know this word so well, I am unlikely to ever forget it
    node = models.ForeignKey(LatticeNode, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "personal vocabulary list entry"
        verbose_name_plural = "personal vocabulary list entries"
        order_with_respect_to = "vocabulary_list"

    def link_job(self):
        return super().link_job(PersonalVocabularyListEntry)

    def data(self):
        return super().data(familiarity=self.familiarity, node=self.node_id)

    def familiarity_range(self):
        # hack for template iteration
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
        unique_nodes = list(set([token["node"] for token in self.text.data]))
        ranked_nodes = [e.node.pk for e in self.vocab_list.entries.filter(node__isnull=False)]
        unranked_nodes = list(filter(lambda node_id: node_id not in ranked_nodes, unique_nodes))

        familiarities = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
        for entry in self.vocab_list.entries.filter(familiarity__isnull=False, node__pk__in=unique_nodes):
            familiarities[str(entry.familiarity)] += 1

        self.unranked = len(unranked_nodes) / len(unique_nodes)
        self.one = familiarities["1"] / len(unique_nodes)
        self.two = familiarities["2"] / len(unique_nodes)
        self.three = familiarities["3"] / len(unique_nodes)
        self.four = familiarities["4"] / len(unique_nodes)
        self.five = familiarities["5"] / len(unique_nodes)

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
