import re
import unicodedata
from typing import List

from django.db import models

from ..models import lookup_form
from .base import BaseService, Preprocessor, Tokenizer, triples


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

# order is optimized for lookup e.g. "ue" is after "que"
LATIN_ENCLITICS = ("que", "ne", "qve", "ve", "ue", "met")


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
            lemmas = lookup_form(word_normalized, "lat")
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

        tokens returns a list of split word + enclitics ex: ['virum', '', 'que']
        """
        text = unicodedata.normalize("NFC", text)
        tokens = re.split(r"(\W+)", text)
        tokens = list(re_tokenize_clitics(tokens))
        return triples(tokens, normalize=latin_periphrastic_normalizer)


class LatinPreprocessor(Preprocessor):
    """
    This is used to apply various prepocessing to the words/tokens before they are further parsed by the lemmatizer
    """
    def preprocessor(self, tokens):
        """
        This function finds the first enclitics attached to the word and returns a list of two strings
        Example:
            tokens = [('virumque', 'virumque', ' ')]
            note: this is following the "(word, word_normalized, following)" tuple format
            virumque will then be broken down into the following:
            Broken into:
            - [(virum, virum, ""), (que, que, " ")]
        """
        new_tokens = []
        found_first_enclitic = False
        for token in tokens:
            word, word_normalized, following = token
            found_form = lookup_form(word, "lat")
            if found_form:
                new_tokens.append(token)
            else:
                found_form_normalized = lookup_form(word_normalized, "lat")
                if found_form_normalized:
                    new_tokens.append(token)
                if not found_form_normalized:
                    for enclitic in LATIN_ENCLITICS:
                        if word.endswith(enclitic) and found_first_enclitic is False:
                            found_first_enclitic = True
                            #Creates example word, word_normalized, following = new_token
                            new_tokens.append((word[:word.find(enclitic)], enclitic, ""))
                            new_tokens.append((enclitic, enclitic, " "))
                            break
                if found_first_enclitic is False and not found_form_normalized:
                    new_tokens.append(token)
        return new_tokens
