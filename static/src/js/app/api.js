import axios from 'axios';

axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.xsrfCookieName = 'csrftoken';

const BASE_URL = '/api/v1/';


export default {
  fetchItems: (id, cb) => {
    return axios.get(`${BASE_URL}texts/${id}/`).then(r => cb(r.data));
  },
};
