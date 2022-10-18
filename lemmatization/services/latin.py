import re
import unicodedata
from typing import List

from ..models import exists_form, lookup_form
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

# Enclitics are particles that "hang on" to the end of latin words.
# Order is optimized for lookup e.g. "ue" is after "que"
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
        # The tokenizers should return doubles: (word, following) instead of triples.
        lemmas = []
        if has_macron(word):
            lemmas = lookup_form(word, "lat")
        if not lemmas:
            lemmas = lookup_form(word_normalized, "lat")
        #Note: this is to fix lookups which contain capitalizations
        if not lemmas:
            lemmas = lookup_form(word_normalized.lower(), "lat")
        return lemmas

    def normalize(self, word):
        """
        For Latin, normalized words are lowercased and macrons are removed.
        """
        word = word.lower()
        if has_macron(word):
            word = strip_macrons(word)
        return word


class LatinTokenizer(Tokenizer):
    """Latin tokenizer.

    Features:
    - Segments latin text into a stream of tokens.
    - A pipe (|) will split words, and an underscore (_) combines words.
    - Tokens are normalized in NFC form.
    - Tokens containing more than one word have any connective/linking words
      automatically stripped from the normalized form (e.g. words in the LATIN_COPULA).
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
    def preprocess(self, tokens):
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
        for token in tokens:
            word, word_normalized, following = token

            # 1. Known word forms should be returned to the token stream unchanged.
            if exists_form(word, "lat") or exists_form(word_normalized, "lat"):
                new_tokens.append(token)
                continue

            # 2. Automatically split off enclitics if the word that precedes the clitic is known.
            found_enclitic = False
            for enclitic in LATIN_ENCLITICS:
                if len(word) > len(enclitic) and word.endswith(enclitic):
                    preceding_word = word[:-len(enclitic)]
                    preceding_word_normalized = word_normalized[:-len(enclitic)]
                    if exists_form(preceding_word, "lat") or exists_form(preceding_word_normalized, "lat"):
                        new_tokens.append((preceding_word, preceding_word_normalized, ""))
                        new_tokens.append((enclitic, enclitic, " "))
                        found_enclitic = True
                        break

            # 3. The token is unknown and does not have an enclitic so return to the token stream unchanged.
            if not found_enclitic:
                new_tokens.append(token)
        return new_tokens
