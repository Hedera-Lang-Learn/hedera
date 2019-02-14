from urllib.parse import urlencode

import requests


def morpheus(form, lang):
    """
    headword/lemma retrieval from the Perseids Morphology Service

    >>> morpheus("λόγος", "grc")
    ['λόγος']
    >>> morpheus("est", "lat")
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
    if r.status_code == 200:
        body = r.json().get("RDF", {}).get("Annotation", {}).get("Body", [])
        if not isinstance(body, list):
            body = [body]
    else:
        body = []

    lemmas = []
    for item in body:
        lemmas.append(item["rest"]["entry"]["dict"]["hdwd"]["$"])

    return lemmas
