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
        Returns an iterable of pairs: (word, following)

        The first item returned will have an empty string for `word` if the
        text starts with a non-word.
        """
        text = unicodedata.normalize("NFC", text)
        tokens = re.split(r"(\W+)", text)
        return pairwise(eveniter(tokens))


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
        # The logic below ensures that accented words aren't split
        # and that certain hyphenated words are treated as a single token.
        # For reference:
        #   0400-04FF is the cyrillic unicode block
        #   0300-036F is the combining diacritical marks block
        text = unicodedata.normalize("NFC", text)  # normalize
        tokens = re.split(r"([^-\u0400-\u04FF\u0300-\u036F]+)", text)
        tokens = self._process(tokens)
        return pairwise(eveniter(tokens))

    def _normalize(self, token):
        token = unicodedata.normalize("NFD", token)
        token = token.translate(self.TRANSLATION_REMOVE_ACCENTS)
        return unicodedata.normalize("NFC", token)

    def _process(self, tokens):
        processed = []
        for token in tokens:
            token = self._normalize(token)
            if "-" in token:
                if token.startswith("по-") or token.endswith("-то"):
                    processed.append(token)
                else:
                    for t in re.split(r"(-)", token):
                        processed.append(t)
            else:
                processed.append(token)
        return processed
