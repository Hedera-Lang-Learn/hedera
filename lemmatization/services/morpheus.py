from urllib.parse import urlencode

import requests

SID = "morpheus"


def lemmatize_word(form, lang):
    """
    headword/lemma retrieval from the Perseids Morphology Service

    >>> lemmatize_word("λόγος", "grc")
    ['λόγος']
    >>> lemmatize_word("est", "lat")
    ['edo1', 'sum1']
    """

    if lang not in ["grc", "lat"]:
        raise ValueError("lang must be one of 'grc' or 'lat'")

    params = {
        "word": form,
        "lang": lang,
        "engine": f"morpheus{lang}",
    }
    qs = urlencode(params)
    url = f"http://services.perseids.org/bsp/morphologyservice/analysis/word?{qs}"
    headers = {
        "Accept": "application/json",
    }
    r = requests.get(url, headers=headers)
    if r.ok:
        body = r.json().get("RDF", {}).get("Annotation", {}).get("Body", [])
        if not isinstance(body, list):
            body = [body]
    else:
        body = []

    lemmas = []
    for item in body:
        lemmas.append(item["rest"]["entry"]["dict"]["hdwd"]["$"])

    return lemmas
