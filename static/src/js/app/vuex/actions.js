import { FETCH_TOKENS, SELECT_TOKEN, FETCH_NODE, UPDATE_TOKEN, SET_TEXT_ID, ADD_LEMMA, FETCH_VOCAB_LISTS, TOGGLE_VOCAB_LIST } from '../constants';
import api from '../api';

export default {
  [FETCH_VOCAB_LISTS]: ({ commit }) => api.fetchVocabLists(data => commit(FETCH_VOCAB_LISTS, data.data)),
  [FETCH_TOKENS]: ({ commit }, { id, vocabList }) => {
    commit(SET_TEXT_ID, id);
    return api.fetchTokens(id, vocabList, data => commit(FETCH_TOKENS, data.data));
  },
  [SELECT_TOKEN]: ({ commit }, { token, index }) => commit(SELECT_TOKEN, { token, index }),
  [FETCH_NODE]: ({ commit }, { id }) => api.fetchNode(id, data => commit(FETCH_NODE, data)),
  [UPDATE_TOKEN]: ({ commit, state }, { id, tokenIndex, nodeId, resolved }) => {
    api.fetchNode(nodeId, data => commit(FETCH_NODE, data));
    return api.updateToken(id, tokenIndex, resolved, state.selectedVocabList, nodeId, null, data => commit(UPDATE_TOKEN, data.data));
  },
  [ADD_LEMMA]: ({ commit, dispatch, state }, { id, tokenIndex, lemma, resolved }) => {
    return api.updateToken(id, tokenIndex, resolved, null, lemma, data => commit(UPDATE_TOKEN, data.data))
      .then(() => {
        dispatch(FETCH_NODE, { id: state.tokens[tokenIndex].node });
      });
  },
  [TOGGLE_VOCAB_LIST]: ({ commit }, { id }) => {
    commit(TOGGLE_VOCAB_LIST, id);
  },
};
