import logging

from hedera.supported_languages import SUPPORTED_LANGUAGES
from lattices.models import LatticeNode, LemmaNode

from .models import add_form, lookup_form


logger = logging.getLogger(__name__)


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
        self._service = SUPPORTED_LANGUAGES[lang].service
        self._tokenizer = SUPPORTED_LANGUAGES[lang].tokenizer
        if self._service is None:
            raise ValueError(f"Lemmatization not supported for language '{lang}''")
        if self._tokenizer is None:
            raise ValueError(f"Tokenization not supported for language '{lang}''")

    def _tokenize(self, text):
        return self._tokenizer.tokenize(text)

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
        context = self._service.SID  # e.g. "morpheus"
        result = []
        tokens = list(self._tokenize(text))
        total_count = len(tokens)
        for index, token in enumerate(tokens):
            word, word_normalized, following = token
            if word_normalized:
                lemmas = self._lemmatize_token(word_normalized)

                # node = get_lattice_node(lemmas, word)  # @@@ not sure what to use for context here

                lemmas = sorted(lemma.rstrip("1") for lemma in lemmas)

                label = " or ".join(lemmas)
                lemma_node = LemmaNode.objects.filter(
                    context=context,
                    lemma=label).first()
                logger.debug(f"lemmatize {context} -> {word} {lemmas} {label}")

                if lemma_node:
                    node = lemma_node.node
                    logger.debug(f"got lemma node {lemma_node.pk} pointing to lattice node {node.pk}")
                else:
                    logger.debug("did not get lemma node")
                    if len(lemmas) > 1:
                        lattice_node = LatticeNode.objects.create(
                            label=label,
                            gloss=f"{context} ambiguity",
                            canonical=False,
                        )
                        for lemma in lemmas:
                            logger.debug(lemma)
                            lemma_node = LemmaNode.objects.filter(
                                context=context,
                                lemma=lemma).first()
                            logger.debug(lemma_node)
                            if lemma_node:
                                child_lattice_node = lemma_node.node
                                lattice_node.children.add(child_lattice_node)
                        lattice_node.save()
                        lemma_node = LemmaNode.objects.create(
                            context=context,
                            lemma=label,
                            node=lattice_node,
                        )
                        children = lattice_node.children.all()
                        logger.debug(f"ambiguous so creating join node {lattice_node.pk} with children {children}")
                        if len(children) == 1:
                            node = children[0]
                        else:
                            node = lattice_node
                    else:
                        node = None

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
                word_normalized=word_normalized,
                following=following,
                node=node_pk,
                resolved=resolved
            ))
            self._report_progress(index, total_count)
        return result
