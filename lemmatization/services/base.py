import requests


class Service(object):

    SID = None
    LANGUAGES = []
    ENDPOINT = ""

    def __init__(self, lang):
        if lang not in self.LANGUAGES:
            raise ValueError(f"lang must be one of {self.LANGUAGES}")
        self.lang = lang

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
