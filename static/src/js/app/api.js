import axios from 'axios';

axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.xsrfCookieName = 'csrftoken';

const BASE_URL = '/api/v1/';


export default {
  fetchItems: (id, cb) => {
    return axios.get(`${BASE_URL}texts/${id}/`).then(r => cb(r.data));
  },
  fetchNode: (id, cb) => {
    return axios.get(`/lattices/${id}.json`).then(r => cb(r.data));
  },
  updateToken: (id, tokenIndex, nodeId, resolved, cb) => {
    return axios.post(`${BASE_URL}texts/${id}/`, { tokenIndex, nodeId, resolved }).then(r => cb(r.data));
  },
};
