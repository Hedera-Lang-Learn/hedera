import requests


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


class BaseService(object):
    SID = None
    LANGUAGES = []

    def __init__(self, lang):
        if lang not in self.LANGUAGES:
            raise ValueError(f"lang must be one of {self.LANGUAGES}")
        self.lang = lang

    def lemmatize(self, form):
        """
        Returns list of lemmas for the given form: [lemma1, lemma2, ...]
        """
        raise NotImplementedError("Must provide implementation on a per service basis.")


class HttpService(BaseService):
    ENDPOINT = ""

    def _headers(self):
        return dict(Accept="application/json")

    def _build_params(self, form):
        raise NotImplementedError("Must provide implementation on a per service basis.")

    def _response_to_lemmas(self, response):
        raise NotImplementedError("Must provide implementation on a per service basis.")

    def _call_service(self, form):
        params = self._build_params(form)
        headers = self._headers()
        response = requests.get(self.ENDPOINT, params=params, headers=headers)
        return self._response_to_lemmas(response)

    def lemmatize(self, form):
        """
        Returns list of lemmas for the given form: [lemma1, lemma2, ...]
        """
        return self._call_service(form)


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

        This method must be overridden.
        """
        raise NotImplementedError("Must provide implementation on a per tokenizer basis.")
