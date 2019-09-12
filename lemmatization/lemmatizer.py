from lattices.utils import get_lattice_node

from .models import add_form, lookup_form
from .services.clancydb import ClancyService
from .services.morpheus import MorpheusService


# from vocab_list.models import VocabularyList

SERVICES = {
    "lat": MorpheusService(lang="lat"),
    "grc": MorpheusService(lang="grc"),
    "rus": ClancyService(lang="rus"),
}


class Lemmatizer(object):

    def __init__(self, lang, cb=None, force_refresh=False):
        self.lang = lang
        self.cb = cb
        self.force_refresh = force_refresh
        self._service = SERVICES.get(lang)
        if self._service is None:
            raise ValueError(f"Lemmatization not supported for language '{lang}''")

    def _tokenize(self, text):
        return self._service.tokenize(text)

    def _lemmatize_token(self, token):
        s = lookup_form(token)
        if not s or self.force_refresh:
            lemmas = self._service.lemmatize(token)
            s |= add_form(
                context=self._service.SID,
                lang=self.lang,
                form=token,
                lemmas=lemmas
            )
        return list(s)

    def _report_progress(self, index, total_count):
        if callable(self.cb):
            self.cb((index + 1) / total_count)

    def lemmatize(self, text):
        result = []
        tokens = list(self._tokenize(text))
        total_count = len(tokens)
        for index, token in enumerate(tokens):
            word, following = token
            if word:
                lemmas = self._lemmatize_token(word)
                node = get_lattice_node(lemmas, word)  # @@@ not sure what to use for context here
                resolved = node and not node.children.exists()
            else:
                node = None
                resolved = None
            node_pk = node.pk if node else None
            result.append(dict(
                word=word,
                following=following,
                node=node_pk,
                resolved=resolved
            ))
            self._report_progress(index, total_count)
        return result


# gnt80 = VocabularyList.objects.get(pk=1)
#
# entry = gnt80.entries.get(lemma="ἄρχω")
# print(entry.lemma, entry.gloss)

# ἄρχω I reign, rule

# entry = gnt80.entries.get(lemma="ἔρχομαι")
# print(entry.lemma, entry.gloss)

# ἔρχομαι I come, go
