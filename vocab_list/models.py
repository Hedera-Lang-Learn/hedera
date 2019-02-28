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
        LatticeNode, null=True, on_delete=models.SET_NULL)

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
