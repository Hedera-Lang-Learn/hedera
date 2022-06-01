import logging

from hedera.supported_languages import SUPPORTED_LANGUAGES

from .models import Lemma, lookup_form


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
        s = lookup_form(token, self.lang)
        # if not s or self.force_refresh:
        #     lemmas = self._service.lemmatize(token)
        #     s |= add_form(
        #         lang=self.lang,
        #         form=token,
        #         lemmas=lemmas
        #     )
        return list(s)

    def _report_progress(self, index, total_count):
        if callable(self.cb):
            self.cb((index + 1) / total_count)

    def lemmatize(self, text):
        result = []
        tokens = list(self._tokenize(text))
        total_count = len(tokens)
        for index, token in enumerate(tokens):
            word, word_normalized, following = token
            lemma_id = None
            if word_normalized:
                lemma_names = self._lemmatize_token(word_normalized)
                lemma_entries = Lemma.objects.filter(lang=self.lang, lemma__in=lemma_names).order_by("rank")
                if len(lemma_entries) == 0:
                    resolved = RESOLVED_NO_LEMMA
                    lemma_id = None
                elif len(lemma_entries) == 1:
                    resolved = RESOLVED_NO_AMBIGUITY
                    lemma_id = lemma_entries[0].pk
                else:
                    resolved = RESOLVED_AUTOMATIC
                    lemma_id = lemma_entries[0].pk  # should be highest frequency lemma

            result.append(dict(
                word=word,
                word_normalized=word_normalized,
                following=following,
                lemma_id=lemma_id,
                glossed=False,  # when True, use specific glosses selected by the teacher
                gloss_ids=[],
                resolved=resolved
            ))
            self._report_progress(index, total_count)
        return result
