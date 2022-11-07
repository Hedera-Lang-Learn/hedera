import re
import unicodedata

from .base import HttpService, Preprocessor, Tokenizer, triples


def maketrans_remove(accents=("COMBINING ACUTE ACCENT", "COMBINING GRAVE ACCENT")):
    """ Makes a translation for removing accents from a string. """
    return str.maketrans("", "", "".join([unicodedata.lookup(a) for a in accents]))


class ClancyService(HttpService):
    """
    headword/lemma retrieval from Steven Clancy's russian database.

    >>> clancy = ClancyService(lang="rus")
    >>> clancy.lemmatize("газету")
    ['газета']
    >>> clancy.lemmatize("дела")
    ['дело', 'деть']
    >>> clancy.lemmatize("ру́сская")
    ['русский']
    >>> clancy.lemmatize("все")
    ['весь', 'все', 'всё']
    >>> clancy.lemmatize("мороженое")
    ['мороженый', 'мороженое']
    """

    SID = "clancy"
    LANGUAGES = ["rus"]
    ENDPOINT = "http://visualizingrussian.fas.harvard.edu/api/lemmatize"

    def _build_params(self, form):
        return dict(word=form)

    def _response_to_lemmas(self, response):
        if response.ok:
            body = response.json().get("data", {}).get("lemmas", [])
            if not isinstance(body, list):
                body = []
        else:
            body = []

        lemmas = [item["label"] for item in body]
        return lemmas


class RUSTokenizer(Tokenizer):
    """
    Tokenizer for Russian.
    """
    TRANSLATION_REMOVE_ACCENTS = maketrans_remove(accents=(
        "COMBINING ACUTE ACCENT",
        "COMBINING GRAVE ACCENT",
        "COMBINING X ABOVE"
    ))

    def tokenize(self, text):
        """
        The logic below ensures that accented words aren't split
        and that certain hyphenated words are treated as a single token.
        For reference:
          0400-04FF is the cyrillic unicode block
          0300-036F is the combining diacritical marks block
        """
        text = unicodedata.normalize("NFC", text)  # normalize
        tokens = re.split(r"([^-\u0400-\u04FF\u0300-\u036F]+)", text)
        tokens = self._split_hyphenated(tokens)
        return triples(tokens, normalize=self._normalize)

    def _normalize(self, token):
        """
        Removes accents from the text.
        """
        token = unicodedata.normalize("NFD", token)
        token = token.translate(self.TRANSLATION_REMOVE_ACCENTS)
        return unicodedata.normalize("NFC", token)

    def _split_hyphenated(self, tokens):
        """
        Splits hyphenated tokens with some exceptions for prefixes/suffixes.
        """
        prefixes = ("по-", "кое-")
        suffixes = ("-либо", "-ка", "-нибудь", "-то")
        processed = []
        for token in tokens:
            if "-" in token:
                w = self._normalize(token)
                if any([w.startswith(s) for s in prefixes]) or any([w.endswith(s) for s in suffixes]):
                    processed.append(token)
                else:
                    for t in re.split(r"(-)", token):
                        processed.append(t)
            else:
                processed.append(token)
        return processed


class RUSPreprocessor(Preprocessor):
    """
    Returns an iterable list of tokens if a custom preprocessor was provided
    This placeholder method can be overridden.
    """
    def preprocess(self, tokens):
        return tokens
