from django.db import models

from .utils import strip_macrons


class FormToLemma(models.Model):
    """
    mapping from surface form to lemma before any lattice consideration

    This can be viewed as a cache of some external lemmatization process.

    The "context" is just an optional label to clarify the source of the
    lookup and should be interpreted the same as in the `lattices` app.
    """

    context = models.CharField(max_length=255, blank=True)
    lang = models.CharField(max_length=3)  # ISO 639.2
    form = models.CharField(max_length=255)
    lemma = models.CharField(max_length=255)

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


class LatinLexicon(models.Model):
    """
    This model contains a copy of the data from LatinMorph16.db
    and is intended to replace the external Perseids Morphology Service
    for the purpose of headword/lemma retrieval.
    """
    token = models.CharField(max_length=255)
    lemma = models.CharField(max_length=255)
    rank = models.IntegerField(default=999999)
    count = models.IntegerField(default=0)
    rate = models.FloatField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["token", "lemma"], name="unique_token_lemma")
        ]


def lookup_form(form, lang=None, contexts=None, annotated=False):
    entries = FormToLemma.objects.filter(form=form)
    if lang:
        entries = entries.filter(lang=lang)
    if contexts:
        entries = entries.filter(context__in=contexts)
    if annotated:
        return entries.values("lemma", "lang", "context")
    else:
        return set(entries.values_list("lemma", flat=True))


def add_form(context, lang, form, lemmas):
    for lemma in lemmas:
        FormToLemma.objects.create(
            context=context,
            lang=lang,
            form=form,
            lemma=lemma,
        )
    return set(lemmas)
