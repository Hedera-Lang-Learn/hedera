import { FETCH_TOKENS, SELECT_TOKEN, FETCH_NODE, UPDATE_TOKEN } from '../constants';
import api from '../api';

export default {
  [FETCH_TOKENS]: ({ commit }, { id }) => api.fetchTokens(id, data => commit(FETCH_TOKENS, data.data)),
  [SELECT_TOKEN]: ({ commit }, { token, index }) => commit(SELECT_TOKEN, { token, index }),
  [FETCH_NODE]: ({ commit }, { id }) => api.fetchNode(id, data => commit(FETCH_NODE, data)),
  [UPDATE_TOKEN]: ({ commit }, { id, tokenIndex, nodeId, resolved }) => {
    api.fetchNode(nodeId, data => commit(FETCH_NODE, data));
    return api.updateToken(id, tokenIndex, nodeId, resolved, data => commit(UPDATE_TOKEN, data.data));
  },
};
