import re

import requests


def pairwise(iterable):
    """s -> (s0, s1), (s2, s3), (s4, s5), ..."""
    a = iter(iterable)
    return zip(a, a)


def tokenize(text):
    """text -> [w0, _, w1, _, w2, _, ...]"""
    tokens = re.split(r"(\W+)", text)
    # test to make sure there is an even number of items in array
    if len(tokens) % 2 > 0:
        tokens.append(" ")
    return tokens


class Service(object):

    SID = None
    LANGUAGES = []
    ENDPOINT = ""

    def __init__(self, lang):
        if lang not in self.LANGUAGES:
            raise ValueError(f"lang must be one of {self.LANGUAGES}")
        self.lang = lang

    def tokenize(self, text):
        """
        Returns pairs of: (word, following)

        The first item returned will have an empty string for `word` if the
        text starts with a non-word.
        """
        return pairwise(tokenize(text))

    def _headers(self):
        return dict(Accept="application/json")

    def _build_params(self, form):
        raise Exception("Must provide implementation on a per service basis.")

    def _response_to_lemmas(self, response):
        raise Exception("Must provide implementation on a per service basis.")

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
