import axios from 'axios';

axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.xsrfCookieName = 'csrftoken';

const BASE_URL = '/api/v1/';

export default {
  fetchMe: (cb) => axios.get(`${BASE_URL}me/`).then((r) => cb(r.data)),
  fetchTexts: (cb) => axios.get(`${BASE_URL}lemmatized_texts/`).then((r) => cb(r.data)),
  fetchText: (id, cb) => axios.get(`${BASE_URL}lemmatized_texts/${id}/detail/`).then((r) => cb(r.data)),
  fetchTextStatus: (id, cb) => axios.get(`${BASE_URL}lemmatized_texts/${id}/status/`).then((r) => cb(r.data)),
  cloneText: (id, cb) => axios.post(`${BASE_URL}lemmatized_texts/${id}/clone/`).then((r) => cb(r.data)),
  textRetryLemmatization: (id, cb) => axios.post(`${BASE_URL}lemmatized_texts/${id}/retry/`).then((r) => cb(r.data)),
  textCancelLemmatization: (id, cb) => axios.post(`${BASE_URL}lemmatized_texts/${id}/cancel/`).then((r) => cb(r.data)),
  fetchPersonalVocabList: (lang) => axios.get(`${BASE_URL}personal_vocab_list/?lang=${lang}`),
  updatePersonalVocabList: (textId, lemmaId, familiarity, headword, definition, entryId, lang) => {
    let data = {
      familiarity, headword, definition, lemmaId,
    };
    if (lang !== null && entryId !== null) {
      return axios.post(`${BASE_URL}personal_vocab_list/${entryId}/?lang=${lang}`, data).then((r) => r.data).catch((error) => error);
    }
    if (entryId !== null) {
      return axios.post(`${BASE_URL}personal_vocab_list/${entryId}/?text=${textId}`, data).then((r) => r.data).catch((error) => error);
    }
    data = { ...data, lemmaId };
    return axios.post(`${BASE_URL}personal_vocab_list/?text=${textId}`, data).then((r) => r.data).catch((error) => error);
  },
  fetchVocabList: (vocabListId) => axios.get(`${BASE_URL}vocab_lists/${vocabListId}`),
  fetchVocabLists: (lang) => axios.get(`${BASE_URL}vocab_lists/?lang=${lang}`),
  fetchVocabEntries: (id, cb) => axios.get(`${BASE_URL}vocab_lists/${id}/entries/`).then((r) => cb(r.data)),
  fetchTokens: (id, vocabList, personalVocabList, cb) => {
    if (!vocabList && !personalVocabList) {
      return axios.get(`${BASE_URL}lemmatized_texts/${id}/`).then((r) => cb(r.data));
    }
    let qs = '';
    if (vocabList) {
      qs = `vocablist_id=${vocabList}`;
    }
    if (personalVocabList) {
      qs = `personalvocablist=${personalVocabList}`;
    }
    return axios.get(`${BASE_URL}lemmatized_texts/${id}/?${qs}`).then((r) => cb(r.data));
  },
  fetchNode: (id, cb) => axios.get(`/lattices/${id}.json`).then((r) => cb(r.data)),
  fetchLemma: (id, cb) => axios.get(`${BASE_URL}lemmatization/lemma/${id}/`).then((r) => cb(r.data)),
  fetchLemmasByForm: (lang, form, cb) => axios.get(`${BASE_URL}lemmatization/forms/${lang}/${encodeURIComponent(form)}/`).then((r) => cb(r.data)),
  fetchLemmasByPartialForm: (lang, form, cb) => axios.get(`${BASE_URL}lemmatization/partial_match_forms/${lang}/${encodeURIComponent(form)}/`).then((r) => cb(r.data)),
  fetchTokenHistory: (id, tokenIndex, cb) => axios.get(`${BASE_URL}lemmatized_texts/${id}/tokens/${tokenIndex}/history/`).then((r) => cb(r.data)),
  updateToken: (id, tokenIndex, resolved, vocabList, lemmaId = null, glossIds = [], lemma = null, cb) => {
    if (vocabList === null) {
      return axios.post(`${BASE_URL}lemmatized_texts/${id}/`, {
        tokenIndex,
        lemmaId,
        glossIds,
        lemma,
        resolved,
      }).then((r) => cb(r.data));
    }
    return axios.post(`${BASE_URL}lemmatized_texts/${id}/?vocablist_id=${vocabList}`, {
      tokenIndex,
      lemmaId,
      glossIds,
      lemma,
      resolved,
    }).then((r) => cb(r.data));
  },
  linkVocabEntry: (id, lemmaId) => axios.post(`${BASE_URL}vocab_entries/${id}/link/`, { lemma_id: lemmaId }),
  updateVocabEntry: (id, headword, definition) => axios.post(`${BASE_URL}vocab_entries/${id}/edit/`, { headword, definition }),
  deleteVocabEntry: (id) => axios.post(`${BASE_URL}vocab_entries/${id}/delete/`),
  fetchPersonalVocabLangList: (cb) => axios.get(`${BASE_URL}personal_vocab_list/quick_add/`).then((r) => cb(r.data)),
  createPersonalVocabEntry: (headword, definition, vocabularyListId, familiarity, lang, lemmaId, cb) => {
    const payload = {
      headword,
      definition,
      familiarity,
      vocabulary_list_id: vocabularyListId,
      lang,
      lemma_id: lemmaId,
    };
    return axios.post(`${BASE_URL}personal_vocab_list/quick_add/`, payload).then((r) => cb(r.data));
  },
  createVocabEntry: (vocabularyListId, headword, definition, lemmaId) => {
    const payload = {
      headword,
      definition,
    };
    if (lemmaId) {
      payload.lemma_id = lemmaId;
    }
    return axios.post(`${BASE_URL}vocab_lists/${vocabularyListId}/entries/`, payload);
  },
  fetchLatticeNodes: (headword, lang, cb) => axios.get(`${BASE_URL}lattice_nodes/?headword=${headword}&lang=${lang}`).then((r) => cb(r.data)),
  updateMeLang: (lang, cb) => axios.post(`${BASE_URL}me/`, { lang }).then((r) => cb(r.data)),
  deletePersonalVocabEntry: (id, cb) => axios.delete(`${BASE_URL}personal_vocab_list/`, { data: { id } }).then((r) => cb(r)),
  fetchBookmarks: (cb) => axios.get(`${BASE_URL}bookmarks/`).then((r) => cb(r.data)),
  addBookmark: (textId) => axios.post(`${BASE_URL}bookmarks/`, { textId }),
  removeBookmark: (bookmarkId) => axios.delete(`${BASE_URL}bookmarks/${bookmarkId}/`),
  fetchSupportedLangList: (cb) => axios.get(`${BASE_URL}supported_languages/`).then((r) => cb(r.data)),
};
