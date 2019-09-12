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
  SET_VOCAB_LIST,
  TOGGLE_SHOW_IN_VOCAB_LIST,
  FETCH_PERSONAL_VOCAB_LIST,
  CREATE_VOCAB_ENTRY,
  UPDATE_VOCAB_ENTRY,
} from '../constants';
import api from '../api';

const logoutOnError = commit => (error) => {
  if (error.response && error.response.status === 401) {
    window.location = '/';
  }
};

export default {
  [FETCH_TEXT]: ({ commit }, { id }) => api
    .fetchText(id, data => commit(FETCH_TEXT, data.data))
    .catch(logoutOnError(commit)),
  [FETCH_VOCAB_LISTS]: ({ commit, state }) => {
    api
      .fetchVocabLists(state.text.lang, data => commit(FETCH_VOCAB_LISTS, data.data))
      .catch(logoutOnError(commit));
  },
  [CREATE_VOCAB_ENTRY]: ({ commit, state }, { nodeId, familiarity, headword, gloss }) => {
    const cb = data => commit(FETCH_PERSONAL_VOCAB_LIST, data.data);
    api
      .updatePersonalVocabList(state.text.id, nodeId, familiarity, headword, gloss, null, cb)
      .catch(logoutOnError(commit));
  },
  // eslint-disable-next-line max-len
  [UPDATE_VOCAB_ENTRY]: ({ commit, state }, { entryId, familiarity, headword, gloss, lang = null }) => {
    const cb = data => commit(FETCH_PERSONAL_VOCAB_LIST, data.data);
    // eslint-disable-next-line max-len
    api
      .updatePersonalVocabList(state.text.id, null, familiarity, headword, gloss, entryId, lang, cb)
      .catch(logoutOnError(commit));
  },
  [FETCH_PERSONAL_VOCAB_LIST]: ({ commit }, { lang }) => {
    const cb = data => commit(FETCH_PERSONAL_VOCAB_LIST, data.data.personalVocabList);
    api
      .fetchPersonalVocabList(lang, cb)
      .catch(logoutOnError(commit));
  },
  [FETCH_TOKENS]: ({ commit }, { id, vocabList, personalVocabList }) => {
    commit(SET_TEXT_ID, id);
    const cb = data => commit(FETCH_TOKENS, data.data);
    return api
      .fetchTokens(id, vocabList, personalVocabList, cb)
      .catch(logoutOnError(commit));
  },
  [SELECT_TOKEN]: ({ commit }, { index }) => commit(SELECT_TOKEN, { index }),
  [FETCH_NODE]: ({ commit }, { id }) => api.fetchNode(id, data => commit(FETCH_NODE, data)),
  [UPDATE_TOKEN]: ({ commit, state }, { id, tokenIndex, nodeId, resolved }) => {
    api
      .fetchNode(nodeId, data => commit(FETCH_NODE, data))
      .catch(logoutOnError(commit));
    const mutate = data => commit(UPDATE_TOKEN, data.data);
    return api
      .updateToken(id, tokenIndex, resolved, state.selectedVocabList, nodeId, null, mutate)
      .catch(logoutOnError(commit));
  },
  [ADD_LEMMA]: ({ commit, dispatch, state }, { id, tokenIndex, lemma, resolved }) => {
    const mutate = data => commit(UPDATE_TOKEN, data.data);
    return api
      .updateToken(id, tokenIndex, resolved, null, null, lemma, mutate)
      .then(() => dispatch(FETCH_NODE, { id: state.tokens[tokenIndex].node }))
      .catch(logoutOnError(commit));
  },
  [SET_VOCAB_LIST]: ({ commit }, { id }) => {
    commit(SET_VOCAB_LIST, id);
  },
  [TOGGLE_SHOW_IN_VOCAB_LIST]: ({ commit }) => {
    commit(TOGGLE_SHOW_IN_VOCAB_LIST);
  },
};
