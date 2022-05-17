from typing import List

from django.db import models

from .utils import strip_macrons


class Lemma(models.Model):
    # TODO: consider indexing alt_lemma and rank
    lang = models.CharField(max_length=3)  # ISO 639.2
    lemma = models.CharField(max_length=255, blank=False)  # Hedera lemma (hic vs hīc)
    alt_lemma = models.CharField(max_length=255, db_index=True)  # Morpheus lemma (hic1 vs hic2)
    label = models.CharField(max_length=255)

    # Lemma frequency data
    rank = models.IntegerField(default=999999)  # Use this as the default sort. Lower rank = more frequent.
    count = models.IntegerField(default=0)  # Higher count = more frequent
    rate = models.FloatField(default=0)  # Higher rate = more frequent.

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["lemma", "lang"], name="unique_lemma_lang")
        ]


class FormToLemma(models.Model):
    """
    mapping from surface form to lemma
    """

    lang = models.CharField(max_length=3)  # ISO 639.2
    form = models.CharField(max_length=255)
    lemma = models.ForeignKey("Lemma", blank=False, on_delete=models.CASCADE, related_name="forms")

    # @@@ do we need created/updated? source?

    @staticmethod
    def load_tab_delimited(fd, context, lang):
        for line in fd:
            form, lemma = line.strip().split("\t")
            FormToLemma.objects.get_or_create(
                context=context,
                lang=lang,
                form=form,
                lemma=lemma,
            )
            FormToLemma.objects.get_or_create(
                context=context,
                lang=lang,
                form=strip_macrons(form),
                lemma=strip_macrons(lemma),
            )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["lang", "form", "lemma"], name="unique_lang_form_lemma")
        ]


class Gloss(models.Model):
    # Note about efficiency:
    #   Consider changing model to many-to-many with Lemma to be more space efficient.
    #   For example: "a", "ab", "abs" each refer to two definitions, but they are the *same* definitions:
    #       by (+abl.)
    #       from,away (+abl.)
    #
    lemma = models.ForeignKey("Lemma", blank=False, on_delete=models.CASCADE, related_name="glosses")
    gloss = models.TextField(max_length=1024)


def lookup_form(form, lang) -> List[str]:
    """ Returns a list of lemmas (strings) in frequency order. """
    entries = FormToLemma.objects.filter(form=form, lang=lang)
    lemma_ids = set(entries.values_list("lemma", flat=True))
    lemmas = Lemma.objects.filter(pk__in=lemma_ids).order_by("rank")
    return list(lemmas.values_list("lemma", flat=True))


def add_form(lang, form, lemmas):
    for lemma in lemmas:
        FormToLemma.objects.create(
            lang=lang,
            form=form,
            lemma=lemma,
        )
    return set(lemmas)
