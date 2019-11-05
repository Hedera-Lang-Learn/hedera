# from lattices.utils import get_lattice_node

from .models import add_form, lookup_form
from .services.clancydb import ClancyService
from .services.morpheus import MorpheusService

from lattices.models import LemmaNode, LatticeNode


# from vocab_list.models import VocabularyList

SERVICES = {
    "lat": MorpheusService(lang="lat"),
    "grc": MorpheusService(lang="grc"),
    "rus": ClancyService(lang="rus"),
}

RESOLVED_NA = "na"
RESOLVED_NO_LEMMA = "no-lemma"
RESOLVED_UNRESOLVED = "unresolved"
RESOLVED_NO_AMBIGUITY = "no-ambiguity"
RESOLVED_AUTOMATIC = "resolved-automatic"
RESOLVED_MANUAL = "resolved-manual"


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

                # node = get_lattice_node(lemmas, word)  # @@@ not sure what to use for context here

                label = " or ".join(lemmas)
                lemma_node = LemmaNode.objects.filter(
                    context="morpheus",
                    lemma=label).first()
                print(word, lemmas, label)

                if lemma_node:
                    node = lemma_node.node
                else:
                    if len(lemmas) > 1:
                        lattice_node = LatticeNode.objects.create(
                            label="morpheus " + label,
                            canonical=False,
                        )
                        for lemma in lemmas:
                            lemma_node = LemmaNode.objects.filter(
                                context="morpheus",
                                lemma=lemma).first()
                            if lemma_node:
                                child_lattice_node = lemma_node.node
                            else:
                                child_lattice_node = LatticeNode.objects.create(
                                    label="morpheus " + lemma,
                                    canonical=False,
                                )
                                lemma_node = LemmaNode.objects.create(
                                    context="morpheus",
                                    lemma=lemma,
                                    node=child_lattice_node,
                                )
                            lattice_node.children.add(child_lattice_node)
                        lattice_node.save()
                        lemma_node = LemmaNode.objects.create(
                            context="morpheus",
                            lemma=label,
                            node=lattice_node,
                        )
                        node = lattice_node
                    else:
                        lattice_node = LatticeNode.objects.create(
                            label="morpheus " + lemma,
                            canonical=False,
                        )
                        lemma_node = LemmaNode.objects.create(
                            context="morpheus",
                            lemma=label,
                            node=lattice_node,
                        )
                        node = lattice_node

                if node:
                    if node.children.exists():
                        resolved = RESOLVED_UNRESOLVED
                    else:
                        resolved = RESOLVED_NO_AMBIGUITY
                else:
                    resolved = RESOLVED_NO_LEMMA
            else:
                node = None
                resolved = RESOLVED_NA
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
