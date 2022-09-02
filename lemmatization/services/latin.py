import re
import unicodedata
from typing import List

from django.db import models

from ..models import lookup_form
from .base import BaseService, Tokenizer, triples


COMBINING_MACRON = unicodedata.lookup("COMBINING MACRON")  # Unicode: 0x0304


def strip_macrons(word):
    """ Returns the word stripped of any combining macrons. """
    return unicodedata.normalize("NFC", "".join(
        ch for ch in unicodedata.normalize("NFD", word) if ch not in [COMBINING_MACRON]
    ))


def has_macron(word):
    """ Returns True if a combining macron exists in the word, False otherwise. """
    return COMBINING_MACRON in unicodedata.normalize("NFD", word)


LATIN_COPULA = [
    "sum", "es", "est", "sumus", "estis", "sunt",
    "eram", "eras", "erat", "eramus", "eratis", "erant",
    "ero", "eris", "erit", "erimus", "eritis", "erunt",
    "sim", "sis", "sit", "simus", "sitis", "sint",
    "siem", "sies", "siet", "siemus", "sietis", "sient",
    "essem", "esses", "esset", "essemus", "essetis", "essent",
    "forem", "fores", "foret", "foremus", "foretis", "forent",
    "esse", "fuisse", "iri", "fore",
]


def latin_periphrastic_normalizer(token):
    token = strip_macrons(token)
    if " " in token:
        return " ".join(word for word in token.split() if word not in LATIN_COPULA)
    else:
        return token


def re_tokenize_clitics(tokens):
    for token in tokens:
        if "_" in token:
            yield token.replace("_", " ")
        elif token == "|":
            yield ""
        else:
            yield token


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


class LatinService(BaseService):
    """
    Latin headword/lemma retrieval

    >>> lat_service = LatinService(lang="lat")
    >>> lat_service.lemmatize("est")
    ['edo', 'sum']
    """

    SID = "morpheus"
    LANGUAGES = ["lat"]

    def lemmatize(self, word: str, word_normalized: str) -> List[str]:
        """
        Retrieves matching lemmas (headwords) for a word by querying our local database of
        latin tokens and lemmas. This was previously a remote call to the remote
        Perseids Morphology Service (e.g. MorpheusService).

        Results are returned in order of highest frequency (rate) first, or simply
        alphabetical by lemma if there is no frequency data.
        """
        # TODO: Move the normalization step HERE instead of the tokenizer.
        # The tokenizers should return doubles: (word, following) instead of triples.
        lemmas = []
        if has_macron(word):
            lemmas = lookup_form(word, "lat")
        if not lemmas:
            lemmas = lookup_form(word_normalized.lower(), "lat")
        return lemmas


class EncliticTokenizer(Tokenizer):
    """
    a tokenizer that
    _
    |
    """

    def tokenize(self, text):
        """
        Returns an iterable of triples: (word, word_normalized, following)

        The first item returned will have an empty string for `word` if the
        text starts with a non-word.
        """
        text = unicodedata.normalize("NFC", text)
        tokens = re.split(r"(\W+)", text)
        tokens = list(re_tokenize_clitics(tokens))
        return triples(tokens, normalize=latin_periphrastic_normalizer)
