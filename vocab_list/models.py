from django.conf import settings
from django.db import models

from lattices.models import LatticeNode
from lattices.utils import make_lemma


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
        verbose_name = "vocabulary list"
        unique_together = [("user", "lang")]

    def __str__(self):
        return f"{self.user} personal vocab list"

    def node_familiarity(self):
        return 10

    def data(self):
        return {
            "words": [w.data() for w in self.entries.all().order_by("headword")]
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

    node = models.ForeignKey(LatticeNode, null=True, on_delete=models.SET_NULL)

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
            headword=self.headword,
            gloss=self.gloss,
            familiarity=self.familiarity
        )
