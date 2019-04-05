from lattices.utils import get_lattice_node

from .models import add_form, lookup_form
from .services import clancydb, morpheus


# from vocab_list.models import VocabularyList

SERVICES = {
    "lat": morpheus,
    "grk": morpheus,
    "rus": clancydb,
}


def lemmatize_word(form, lang, force_refresh=False):
    s = lookup_form(form)
    if not s or force_refresh:
        service = SERVICES.get(lang)
        if service:
            s |= add_form(service.SID, lang, form, service.lemmatize_word(form, lang))
        else:
            raise ValueError(f"Lemmatization not supported for language '{lang}''")
    return list(s)


def lemmatize_text(text, lang, cb=None):
    result = []
    tokens = text.split()
    total_count = len(tokens)
    for index, token in enumerate(tokens):
        lemmas = lemmatize_word(token.strip(",.?:;·"), lang)
        node = get_lattice_node(lemmas, token)  # @@@ not sure what to use for context here
        if not node or node.children.exists():
            resolved = False
        else:
            resolved = True
        if node:
            node_pk = node.pk
        else:
            node_pk = None
        result.append({"token": token, "node": node_pk, "resolved": resolved})
        if callable(cb):
            cb((index + 1) / total_count)
    return result


# gnt80 = VocabularyList.objects.get(pk=1)
#
# entry = gnt80.entries.get(lemma="ἄρχω")
# print(entry.lemma, entry.gloss)

# ἄρχω I reign, rule

# entry = gnt80.entries.get(lemma="ἔρχομαι")
# print(entry.lemma, entry.gloss)

# ἔρχομαι I come, go
