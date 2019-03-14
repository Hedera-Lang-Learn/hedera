/* eslint-disable object-curly-newline */
import {
  FETCH_TEXT,
  FETCH_TOKENS,
  SELECT_TOKEN,
  FETCH_NODE,
  UPDATE_TOKEN,
  SET_TEXT_ID,
  ADD_LEMMA,
  FETCH_VOCAB_LISTS,
  TOGGLE_VOCAB_LIST,
  TOGGLE_SHOW_IN_VOCAB_LIST,
  FETCH_PERSONAL_VOCAB_LIST,
  CREATE_VOCAB_ENTRY,
  UPDATE_VOCAB_ENTRY,
} from '../constants';
import api from '../api';

export default {
  [FETCH_TEXT]: ({ commit }, { id }) => api.fetchText(id, data => commit(FETCH_TEXT, data.data)),
  [FETCH_VOCAB_LISTS]: ({ commit, state }) => {
    api.fetchVocabLists(state.text.lang, data => commit(FETCH_VOCAB_LISTS, data.data));
  },
  [CREATE_VOCAB_ENTRY]: ({ commit, state }, { nodeId, familiarity, headword, gloss }) => {
    return api.updatePersonalVocabList(state.text.lang, nodeId, familiarity, headword, gloss, null, (data) => {
      commit(FETCH_PERSONAL_VOCAB_LIST, data.data);
    });
  },
  [UPDATE_VOCAB_ENTRY]: ({ commit, state }, { entryId, familiarity, headword, gloss }) => {
    return api.updatePersonalVocabList(state.text.lang, null, familiarity, headword, gloss, entryId, (data) => {
      commit(FETCH_PERSONAL_VOCAB_LIST, data.data);
    });
  },
  [FETCH_PERSONAL_VOCAB_LIST]: ({ commit, state }) => {
    api.fetchPersonalVocabList(state.text.lang, data => commit(FETCH_PERSONAL_VOCAB_LIST, data.data));
  },
  [FETCH_TOKENS]: ({ commit }, { id, vocabList, personalVocabList }) => {
    commit(SET_TEXT_ID, id);
    return api.fetchTokens(id, vocabList, personalVocabList, data => commit(FETCH_TOKENS, data.data));
  },
  [SELECT_TOKEN]: ({ commit }, { index }) => commit(SELECT_TOKEN, { index }),
  [FETCH_NODE]: ({ commit }, { id }) => api.fetchNode(id, data => commit(FETCH_NODE, data)),
  [UPDATE_TOKEN]: ({ commit, state }, { id, tokenIndex, nodeId, resolved }) => {
    api.fetchNode(nodeId, data => commit(FETCH_NODE, data));
    const mutate = data => commit(UPDATE_TOKEN, data.data);
    return api.updateToken(id, tokenIndex, resolved, state.selectedVocabList, nodeId, null, mutate);
  },
  [ADD_LEMMA]: ({ commit, dispatch, state }, { id, tokenIndex, lemma, resolved }) => {
    const mutate = data => commit(UPDATE_TOKEN, data.data);
    return api.updateToken(id, tokenIndex, resolved, null, lemma, mutate)
      .then(() => dispatch(FETCH_NODE, { id: state.tokens[tokenIndex].node }));
  },
  [TOGGLE_VOCAB_LIST]: ({ commit }, { id }) => {
    commit(TOGGLE_VOCAB_LIST, id);
  },
  [TOGGLE_SHOW_IN_VOCAB_LIST]: ({ commit }) => {
    commit(TOGGLE_SHOW_IN_VOCAB_LIST);
  },
};
