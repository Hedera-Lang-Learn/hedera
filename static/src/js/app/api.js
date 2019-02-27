import axios from 'axios';

axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.xsrfCookieName = 'csrftoken';

const BASE_URL = '/api/v1/';


export default {
  fetchTokens: (id, cb) => {
    return axios.get(`${BASE_URL}lemmatized_texts/${id}/`).then(r => cb(r.data));
  },
  fetchNode: (id, cb) => {
    return axios.get(`/lattices/${id}.json`).then(r => cb(r.data));
  },
  updateToken: (id, tokenIndex, resolved, nodeId = null, lemma = null, cb) => {
    return axios.post(`${BASE_URL}lemmatized_texts/${id}/`, { tokenIndex, nodeId, lemma, resolved }).then(r => cb(r.data));
  },
};
