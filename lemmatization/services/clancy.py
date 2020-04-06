from .base import Service


class ClancyService(Service):
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
