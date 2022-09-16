import logging

from hedera.supported_languages import SUPPORTED_LANGUAGES

from .models import Lemma


logger = logging.getLogger(__name__)


RESOLVED_NA = "na"
RESOLVED_NO_LEMMA = "no-lemma"
RESOLVED_UNRESOLVED = "unresolved"
RESOLVED_NO_AMBIGUITY = "no-ambiguity"
RESOLVED_AUTOMATIC = "resolved-automatic"
RESOLVED_MANUAL = "resolved-manual"

GLOSSED_NA = "na"
GLOSSED_AUTOMATIC = "glossed-automatic"
GLOSSED_MANUAL = "glossed-manual"


class Lemmatizer(object):

    def __init__(self, lang, cb=None, force_refresh=False):
        self.lang = lang
        self.cb = cb
        self.force_refresh = force_refresh
        self._service = SUPPORTED_LANGUAGES[lang].service
        self._tokenizer = SUPPORTED_LANGUAGES[lang].tokenizer
        self._preprocessor = SUPPORTED_LANGUAGES[lang].preprocessor
        if self._service is None:
            raise ValueError(f"Lemmatization not supported for language '{lang}''")
        if self._tokenizer is None:
            raise ValueError(f"Tokenization not supported for language '{lang}''")
        if self._preprocessor is None:
            raise ValueError(f"Preprocessor not supported for language '{lang}''")

    def _tokenize(self, text):
        return self._tokenizer.tokenize(text)

    def _preprocess(self, tokens):
        return self._preprocessor.preprocess(tokens)

    def _lemmatize(self, word, word_normalized):
        lemmas = self._service.lemmatize(word, word_normalized)
        return list(lemmas)

    def _report_progress(self, index, total_count):
        if callable(self.cb):
            self.cb((index + 1) / total_count)

    def lemmatize(self, text):
        result = []
        tokens = list(self._tokenize(text))
        tokens = self._preprocess(tokens)
        total_count = len(tokens)
        for index, token in enumerate(tokens):
            word, word_normalized, following = token
            lemma_id = None
            gloss_ids = []
            glossed = GLOSSED_NA
            resolved = RESOLVED_NA
            if word_normalized:
                lemma_names = self._lemmatize(word, word_normalized)
                lemma_entries = Lemma.objects.filter(lang=self.lang, lemma__in=lemma_names).order_by("rank")

                # automatically select the highest frequency lemma
                # assumes that the lemma entries are ranked in frequency order, highest frequency first
                if len(lemma_entries) == 0:
                    resolved = RESOLVED_NO_LEMMA
                    lemma_id = None
                elif len(lemma_entries) == 1:
                    resolved = RESOLVED_NO_AMBIGUITY
                    lemma_id = lemma_entries[0].pk
                else:
                    resolved = RESOLVED_AUTOMATIC
                    lemma_id = lemma_entries[0].pk

                # automatically select all glosses for the lemma
                # this can be changed later by manually selecting glosses if desired
                if lemma_id:
                    gloss_ids = [gloss.pk for gloss in lemma_entries[0].glosses.all()]
                    glossed = GLOSSED_AUTOMATIC

            result.append(dict(
                word=word,
                word_normalized=word_normalized,
                following=following,
                lemma_id=lemma_id,
                gloss_ids=gloss_ids,
                glossed=glossed,
                resolved=resolved
            ))
            self._report_progress(index, total_count)
        return result
