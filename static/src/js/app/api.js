import axios from 'axios';

axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.xsrfCookieName = 'csrftoken';

const BASE_URL = '/api/v1/';


export default {
  fetchText: (id, cb) => axios.get(`${BASE_URL}lemmatized_texts/${id}/detail/`).then(r => cb(r.data)),
  fetchPersonalVocabList: (lang, cb) => axios.get(`${BASE_URL}personal_vocab_list/?lang=${lang}`).then(r => cb(r.data)),
  updatePersonalVocabList: (lang, nodeId, familiarity, headword, gloss, entryId, cb) => {
    let data = { familiarity, headword, gloss };
    if (entryId !== null) {
      return axios.post(`${BASE_URL}personal_vocab_list/${entryId}/?lang=${lang}`, data).then(r => cb(r.data));
    }
    data = { ...data, nodeId };
    return axios.post(`${BASE_URL}personal_vocab_list/?lang=${lang}`, data).then(r => cb(r.data));
  },
  fetchVocabLists: (lang, cb) => axios.get(`${BASE_URL}vocab_lists/?lang=${lang}`).then(r => cb(r.data)),
  fetchTokens: (id, vocabList, personalVocabList, cb) => {
    if (!vocabList && !personalVocabList) {
      return axios.get(`${BASE_URL}lemmatized_texts/${id}/`).then(r => cb(r.data));
    }
    let qs = '';
    if (vocabList) {
      qs = `vocablist=${vocabList}`;
    }
    if (personalVocabList) {
      qs = `personalvocablist=${personalVocabList}`;
    }
    return axios.get(`${BASE_URL}lemmatized_texts/${id}/?${qs}`).then(r => cb(r.data));
  },
  fetchNode: (id, cb) => axios.get(`/lattices/${id}.json`).then(r => cb(r.data)),
  updateToken: (id, tokenIndex, resolved, vocabList, nodeId = null, lemma = null, cb) => {
    if (vocabList === null) {
      return axios.post(`${BASE_URL}lemmatized_texts/${id}/`, {
        tokenIndex,
        nodeId,
        lemma,
        resolved,
      }).then(r => cb(r.data));
    }
    return axios.post(`${BASE_URL}lemmatized_texts/${id}/?vocablist=${vocabList}`, {
      tokenIndex,
      nodeId,
      lemma,
      resolved,
    }).then(r => cb(r.data));
  },
};
