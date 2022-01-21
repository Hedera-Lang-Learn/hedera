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
  fetchPersonalVocabList: (lang, cb) => axios.get(`${BASE_URL}personal_vocab_list/?lang=${lang}`).then((r) => cb(r.data)),
  updatePersonalVocabList: (textId, nodeId, familiarity, headword, gloss, entryId, lang, cb) => {
    let data = { familiarity, headword, gloss };
    if (lang !== null && entryId !== null) {
      return axios.post(`${BASE_URL}personal_vocab_list/${entryId}/?lang=${lang}`, data).then((r) => cb(r.data));
    }
    if (entryId !== null) {
      return axios.post(`${BASE_URL}personal_vocab_list/${entryId}/?text=${textId}`, data).then((r) => cb(r.data));
    }
    data = { ...data, nodeId };
    return axios.post(`${BASE_URL}personal_vocab_list/?text=${textId}`, data).then((r) => cb(r.data));
  },
  fetchVocabLists: (lang, cb) => axios.get(`${BASE_URL}vocab_lists/?lang=${lang}`).then((r) => cb(r.data)),
  fetchVocabEntries: (id, cb) => axios.get(`${BASE_URL}vocab_lists/${id}/entries/`).then((r) => cb(r.data)),
  fetchTokens: (id, vocabList, personalVocabList, cb) => {
    if (!vocabList && !personalVocabList) {
      return axios.get(`${BASE_URL}lemmatized_texts/${id}/`).then((r) => cb(r.data));
    }
    let qs = '';
    if (vocabList) {
      qs = `vocablist=${vocabList}`;
    }
    if (personalVocabList) {
      qs = `personalvocablist=${personalVocabList}`;
    }
    return axios.get(`${BASE_URL}lemmatized_texts/${id}/?${qs}`).then((r) => cb(r.data));
  },
  fetchNode: (id, cb) => axios.get(`/lattices/${id}.json`).then((r) => cb(r.data)),
  fetchTokenHistory: (id, tokenIndex, cb) => axios.get(`${BASE_URL}lemmatized_texts/${id}/tokens/${tokenIndex}/history/`).then((r) => cb(r.data)),
  updateToken: (id, tokenIndex, resolved, vocabList, nodeId = null, lemma = null, cb) => {
    if (vocabList === null) {
      return axios.post(`${BASE_URL}lemmatized_texts/${id}/`, {
        tokenIndex,
        nodeId,
        lemma,
        resolved,
      }).then((r) => cb(r.data));
    }
    return axios.post(`${BASE_URL}lemmatized_texts/${id}/?vocablist=${vocabList}`, {
      tokenIndex,
      nodeId,
      lemma,
      resolved,
    }).then((r) => cb(r.data));
  },
  vocabEntryLink: (id, node, cb) => axios.post(`${BASE_URL}vocab_entries/${id}/link/`, { node }).then((r) => cb(r.data)),
  vocabEntryEdit: (id, headword, gloss, cb) => axios.post(`${BASE_URL}vocab_entries/${id}/edit/`, { headword, gloss }).then((r) => cb(r.data)),
  vocabEntryDelete: (id, cb) => axios.post(`${BASE_URL}vocab_entries/${id}/delete/`).then((r) => cb(r.data)),
  fetchPersonalVocabLangList: (cb) => axios.get(`${BASE_URL}personal_vocab_list/quick_add/`).then((r) => cb(r.data)),
  createPersonalVocabEntry: (headword, gloss, vocabularyListId, familiarity, node, lang, cb) => axios.post(`${BASE_URL}personal_vocab_list/quick_add/`, {
    headword, gloss, familiarity, vocabulary_list_id: vocabularyListId, node, lang,
  }).then((r) => cb(r.data)),
  fetchLatticeNodes: (headword, lang, cb) => axios.get(`${BASE_URL}lattice_nodes/?headword=${headword}&lang=${lang}`).then((r) => cb(r.data)),
  updateMeLang: (lang, cb) => axios.post(`${BASE_URL}me/`, { lang }).then((r) => cb(r.data)),
  deletePersonalVocabEntry: (id, cb) => axios.delete(`${BASE_URL}personal_vocab_list/`, { data: { id } }).then((r) => cb(r)),
  fetchBookmarks: (cb) => axios.get(`${BASE_URL}bookmarks/`).then((r) => cb(r.data)),
  addBookmark: (textId) => axios.post(`${BASE_URL}bookmarks/`, { textId }),
  removeBookmark: (bookmarkId) => axios.delete(`${BASE_URL}bookmarks/${bookmarkId}/`),
  fetchSupportedLangList: (cb) => axios.get(`${BASE_URL}supported_languages/`).then((r) => cb(r.data)),
};
