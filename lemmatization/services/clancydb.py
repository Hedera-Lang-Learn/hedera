from urllib.parse import urlencode

import requests

SID = "clancydb"

def lemmatize_word(form, lang):
    """
    headword/lemma retrieval from Steven Clancy's russian database.

    >>> lemmatize_word("газету", "rus")
    ['газета']
    >>> lemmatize_word("дела", "rus")
    ['дело', 'деть']
    >>> lemmatize_word("ру́сская", "rus")
    ['русский']
    >>> lemmatize_word("все", "rus")
    ['весь', 'все', 'всё']
    >>> lemmatize_word("мороженое", "rus")
    ['мороженый', 'мороженое']
    """
    if lang != "rus":
        raise ValueError("lang must be one of 'rus'")

    params = {"word": form}
    qs = urlencode(params)
    url = f"http://visualizingrussian.fas.harvard.edu/api/lemmatize?{qs}"
    headers = {
        "Accept": "application/json",
    }
    r = requests.get(url, headers=headers)
    if r.ok:
        body = r.json().get("data", {}).get("lemmas", [])
        if not isinstance(body, list):
            body = [] 
    else:
        body = []

    lemmas = [item["label"] for item in body]
    return lemmas

