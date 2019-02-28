import axios from 'axios';

axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.xsrfCookieName = 'csrftoken';

const BASE_URL = '/api/v1/';


export default {
  fetchVocabLists: cb => axios.get(`${BASE_URL}vocab_lists/`).then(r => cb(r.data)),
  fetchTokens: (id, vocabList, cb) => {
    if (vocabList === null) {
      return axios.get(`${BASE_URL}lemmatized_texts/${id}/`).then(r => cb(r.data));
    }
    return axios.get(`${BASE_URL}lemmatized_texts/${id}/?vocablist=${vocabList}`).then(r => cb(r.data));
  },
  fetchNode: (id, cb) => {
    return axios.get(`/lattices/${id}.json`).then(r => cb(r.data));
  },
  updateToken: (id, tokenIndex, resolved, vocabList, nodeId = null, lemma = null, cb) => {
    if (vocabList === null) {
      return axios.post(`${BASE_URL}lemmatized_texts/${id}/`, { tokenIndex, nodeId, lemma, resolved }).then(r => cb(r.data));
    }
    return axios.post(`${BASE_URL}lemmatized_texts/${id}/?vocablist=${vocabList}`, { tokenIndex, nodeId, lemma, resolved }).then(r => cb(r.data));
  },
};
