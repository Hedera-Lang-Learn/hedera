import re
import unicodedata

from .base import Tokenizer, triples
from .morpheus import MorpheusService


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


class LatinService(MorpheusService):
    lang = "lat"


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
