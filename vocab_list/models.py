from django.conf import settings
from django.db import models

from lattices.models import LatticeNode
from lattices.utils import make_lemma
from lemmatized_text.models import LemmatizedText

from iso639 import languages


class VocabularyList(models.Model):

    # a NULL owner means a system-provided vocabulary list
    owner = models.ForeignKey(
        getattr(settings, "AUTH_USER_MODEL", "auth.User"),
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    lang = models.CharField(max_length=3)  # ISO 639.2

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    cloned_from = models.ForeignKey(
        "self", null=True, editable=False, on_delete=models.SET_NULL
    )

    def load_tab_delimited(self, fd):
        for line in fd:
            headword, gloss = line.strip().split("\t")
            VocabularyListEntry.objects.create(
                vocabulary_list=self,
                headword=headword,
                gloss=gloss
            )

    class Meta:
        verbose_name = "vocabulary list"

    def __str__(self):
        return self.title

    def language_name(self):
        return languages.get(part3=self.lang).name

    def data(self):
        return {
            "id": self.pk,
            "title": self.title,
            "description": self.description,
        }


class VocabularyListEntry(models.Model):

    vocabulary_list = models.ForeignKey(
        VocabularyList, related_name="entries", on_delete=models.CASCADE)

    headword = models.CharField(max_length=255)
    gloss = models.TextField(blank=True)

    node = models.ForeignKey(
        LatticeNode, related_name="vocabulary_entries", null=True, on_delete=models.SET_NULL)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "vocabulary list entry"
        verbose_name_plural = "vocabulary list entries"
        order_with_respect_to = "vocabulary_list"
        unique_together = ("vocabulary_list", "headword")

    def link_node(self):
        if self.node is None:
            self.node = make_lemma(self.headword)  # context?
            self.save()


class PersonalVocabularyList(models.Model):

    user = models.ForeignKey(
        getattr(settings, "AUTH_USER_MODEL", "auth.User"),
        on_delete=models.CASCADE
    )
    lang = models.CharField(max_length=3)  # ISO 639.2

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "personal vocabulary list"
        unique_together = [("user", "lang")]

    def __str__(self):
        return f"{self.user} personal {self.lang} vocab list"

    def node_familiarity(self):
        return 10

    def data(self):
        stats = {}
        for stat in self.personalvocabularystats_set.all():
            stats[stat.text.pk] = stat.data()
        return {
            "entries": [w.data() for w in self.entries.all().order_by("headword")],
            "statsByText": stats,
        }


class PersonalVocabularyListEntry(models.Model):

    vocabulary_list = models.ForeignKey(
        PersonalVocabularyList,
        related_name="entries",
        on_delete=models.CASCADE
    )

    headword = models.CharField(max_length=255)
    gloss = models.TextField(blank=True)

    # 1. I don't recognise this word
    # 2. I recognise this word but don't know what it means
    # 3. I think I know what this word means
    # 4. I definitely know what this word means but could forget soon
    # 5. I know this word so well, I am unlikely to ever forget it

    familiarity = models.IntegerField(null=True)

    node = models.ForeignKey(LatticeNode, null=True, blank=True, on_delete=models.SET_NULL)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "personal vocabulary list entry"
        verbose_name_plural = "personal vocabulary list entries"
        order_with_respect_to = "vocabulary_list"
        unique_together = ("vocabulary_list", "headword")

    def link_node(self):
        if self.node is None:
            self.node = make_lemma(self.headword)  # context?
            self.save()

    def data(self):
        return dict(
            id=self.pk,
            headword=self.headword,
            gloss=self.gloss,
            familiarity=self.familiarity,
            node=self.node.pk if self.node is not None else None,
        )

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
