import re
import unicodedata


def pairwise(iterable):
    """s -> (s0, s1), (s2, s3), (s4, s5), ..."""
    a = iter(iterable)
    return zip(a, a)


def eveniter(iterable, last=" "):
    """ Generates an even number of values. """
    even = True
    for value in iterable:
        even = not even
        yield value
    if not even:
        yield last


def triples(tokens, normalize=None):
    pairs = pairwise(eveniter(tokens))
    for token, following in pairs:
        if normalize is None:
            yield token, token, following
        else:
            yield token, normalize(token), following


def maketrans_remove(accents=("COMBINING ACUTE ACCENT", "COMBINING GRAVE ACCENT")):
    """ Makes a translation for removing accents from a string. """
    return str.maketrans("", "", "".join([unicodedata.lookup(a) for a in accents]))


class Tokenizer(object):
    """
    Tokenizer for breaking text into a list of tokens.

    Subclasses should override the tokenize() method to provide
    language-specific tokenization.
    """

    def __init__(self, lang):
        self.lang = lang

    def tokenize(self, text):
        """
        Returns an iterable of triples: (word, word_normalized, following)

        The first item returned will have an empty string for `word` if the
        text starts with a non-word.
        """
        text = unicodedata.normalize("NFC", text)
        tokens = re.split(r"(\W+)", text)
        return triples(tokens)


class LATTokenizer(Tokenizer):
    """
    Tokenizer for Latin.
    """
    TRANSLATION_SPELLING = str.maketrans("jJuU", "iIvV")

    def tokenize(self, text):
        """
        Returns an iterable of triples: (word, word_normalized, following)
        """
        text = unicodedata.normalize("NFC", text)
        tokens = re.split(r"(\W+)", text)
        return triples(tokens, normalize=self._normalize)

    def _normalize(self, token):
        """
        Normalizes spelling (j->i, u->v).
        """
        return token.translate(self.TRANSLATION_SPELLING)


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
