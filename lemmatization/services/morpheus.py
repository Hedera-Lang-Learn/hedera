import unicodedata

from .base import Service


def strip_macrons(word):
    return unicodedata.normalize("NFC", "".join(
        ch for ch in unicodedata.normalize("NFD", word) if ch not in ["\u0304"]
    ))


class MorpheusService(Service):
    """
    headword/lemma retrieval from the Perseids Morphology Service

    >>> morpheus_grc = MorpheusService(lang="grc")
    >>> morpheus_grc.lemmatize("λόγος")
    ['λόγος']

    >>> morpheus_lat = MorpheusService(lang="lat")
    >>> morpheus_lat.lemmatize("est")
    ['edo1', 'sum1']
    """

    SID = "morpheus"
    LANGUAGES = ["grc", "lat"]
    ENDPOINT = "http://services.perseids.org/bsp/morphologyservice/analysis/word"

    def _build_params(self, form):
        if self.lang == "lat":
            form = strip_macrons(form)
        return dict(word=form, lang=self.lang, engine=f"morpheus{self.lang}")

    def _response_to_lemmas(self, response):
        if response.ok:
            body = response.json().get("RDF", {}).get("Annotation", {}).get("Body", [])
            if not isinstance(body, list):
                body = [body]
        else:
            body = []

        lemmas = []
        for item in body:
            lemmas.append(item["rest"]["entry"]["dict"]["hdwd"]["$"])
        return lemmas
