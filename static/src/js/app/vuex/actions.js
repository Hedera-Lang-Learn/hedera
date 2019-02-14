import { FETCH_ITEMS, SELECT_TOKEN, FETCH_NODE, UPDATE_TOKEN } from '../constants';
import api from '../api';

export default {
  [FETCH_ITEMS]: ({ commit }, { id }) => api.fetchItems(id, data => commit(FETCH_ITEMS, data.data)),
  [SELECT_TOKEN]: ({ commit }, { token, index }) => commit(SELECT_TOKEN, { token, index }),
  [FETCH_NODE]: ({ commit }, { id }) => api.fetchNode(id, data => commit(FETCH_NODE, data)),
  [UPDATE_TOKEN]: ({ commit }, { id, tokenIndex, nodeId }) => api.updateToken(id, tokenIndex, nodeId, data => commit(UPDATE_TOKEN, data.data)),
};
