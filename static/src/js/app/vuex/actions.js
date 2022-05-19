/* eslint-disable object-curly-newline */
import {
  FETCH_TEXT,
  FETCH_TOKENS,
  SELECT_TOKEN,
  FETCH_NODE,
  FETCH_LEMMA,
  FETCH_LEMMAS_BY_FORM,
  UPDATE_TOKEN,
  SET_TEXT_ID,
  ADD_LEMMA,
  FETCH_VOCAB_LISTS,
  SET_VOCAB_LIST,
  TOGGLE_SHOW_IN_VOCAB_LIST,
  FETCH_PERSONAL_VOCAB_LIST,
  CREATE_VOCAB_ENTRY,
  UPDATE_VOCAB_ENTRY,
  FETCH_ME,
  FETCH_PERSONAL_VOCAB_LANG_LIST,
  CREATE_PERSONAL_VOCAB_ENTRY,
  FETCH_LATTICE_NODES_BY_HEADWORD,
  RESET_LATTICE_NODES_BY_HEADWORD,
  SET_LANGUAGE_PREF,
  DELETE_PERSONAL_VOCAB_ENTRY,
  FETCH_BOOKMARKS,
  ADD_BOOKMARK,
  REMOVE_BOOKMARK,
  FETCH_SUPPORTED_LANG_LIST,
} from '../constants';
import api from '../api';

// eslint-disable-next-line no-unused-vars
const logoutOnError = (commit) => (error) => {
  if (error.response && error.response.status === 401) {
    window.location = '/';
  }
};

export default {
  [FETCH_ME]: ({ commit }) => api.fetchMe((data) => commit(FETCH_ME, data.data)),
  [FETCH_TEXT]: ({ commit }, { id }) => api
    .fetchText(id, (data) => commit(FETCH_TEXT, data.data))
    .catch(logoutOnError(commit)),
  [FETCH_VOCAB_LISTS]: ({ commit, state }) => {
    api
      .fetchVocabLists(state.text.lang, (data) => commit(FETCH_VOCAB_LISTS, data.data))
      .catch(logoutOnError(commit));
  },
  [CREATE_VOCAB_ENTRY]: ({ commit, state }, { nodeId, familiarity, headword, gloss }) => {
    const cb = (data) => commit(FETCH_PERSONAL_VOCAB_LIST, data.data);
    api
      .updatePersonalVocabList(state.text.id, nodeId, familiarity, headword, gloss, null, null, cb)
      .catch(logoutOnError(commit));
  },
  // eslint-disable-next-line max-len
  [UPDATE_VOCAB_ENTRY]: ({ commit, state }, { entryId, familiarity, headword, gloss, lang = null }) => {
    const cb = (data) => commit(FETCH_PERSONAL_VOCAB_LIST, data.data);
    // eslint-disable-next-line max-len
    api
      .updatePersonalVocabList(state.text.id, null, familiarity, headword, gloss, entryId, lang, cb)
      .catch(logoutOnError(commit));
  },
  [FETCH_PERSONAL_VOCAB_LIST]: ({ commit }, { lang }) => {
    const cb = (data) => commit(FETCH_PERSONAL_VOCAB_LIST, data.data.personalVocabList);
    api
      .fetchPersonalVocabList(lang, cb)
      .catch(logoutOnError(commit));
  },
  [FETCH_TOKENS]: ({ commit }, { id, vocabList, personalVocabList }) => {
    commit(SET_TEXT_ID, id);
    const cb = (data) => commit(FETCH_TOKENS, data.data);
    return api
      .fetchTokens(id, vocabList, personalVocabList, cb)
      .catch(logoutOnError(commit));
  },
  [SELECT_TOKEN]: ({ commit, state }, { token }) => api.fetchTokenHistory(
    state.textId,
    token.tokenIndex,
    (data) => commit(SELECT_TOKEN, { token, data }),
  ),
  [FETCH_NODE]: ({ commit }, { id }) => api.fetchNode(id, (data) => commit(FETCH_NODE, data)),
  [FETCH_LEMMA]: ({ commit }, { id }) => api.fetchLemma(id, (data) => commit(FETCH_LEMMA, data)),
  [FETCH_LEMMAS_BY_FORM]: ({ commit }, { lang, form }) => api.fetchLemmasByForm(lang, form, (data) => commit(FETCH_LEMMAS_BY_FORM, data)),
  [UPDATE_TOKEN]: ({ commit, state }, { id, tokenIndex, nodeId, resolved }) => {
    api
      .fetchNode(nodeId, (data) => commit(FETCH_NODE, data))
      .catch(logoutOnError(commit));
    const mutate = (data) => commit(UPDATE_TOKEN, data.data);
    return api
      .updateToken(id, tokenIndex, resolved, state.selectedVocabList, nodeId, null, mutate)
      .catch(logoutOnError(commit));
  },
  [ADD_LEMMA]: ({ commit, dispatch, state }, { id, tokenIndex, lemma, resolved }) => {
    const mutate = (data) => commit(UPDATE_TOKEN, data.data);
    return api
      .updateToken(id, tokenIndex, resolved, null, state.selectedToken.node, lemma, mutate)
      .then(() => dispatch(FETCH_NODE, { id: state.tokens[tokenIndex].node }))
      .catch(logoutOnError(commit));
  },
  [SET_VOCAB_LIST]: ({ commit }, { id }) => {
    commit(SET_VOCAB_LIST, id);
  },
  [TOGGLE_SHOW_IN_VOCAB_LIST]: ({ commit }) => {
    commit(TOGGLE_SHOW_IN_VOCAB_LIST);
  },
  [FETCH_PERSONAL_VOCAB_LANG_LIST]: ({ commit }) => {
    const cb = (data) => commit(FETCH_PERSONAL_VOCAB_LANG_LIST, data.data);
    return api
      .fetchPersonalVocabLangList(cb)
      .catch(logoutOnError(commit));
  },
  [CREATE_PERSONAL_VOCAB_ENTRY]: ({ commit }, { headword, gloss, vocabularyListId, familiarity, node, lang }) => {
    const cb = (data) => commit(CREATE_PERSONAL_VOCAB_ENTRY, data.data);
    return api
      .createPersonalVocabEntry(headword, gloss, vocabularyListId, familiarity, node, lang, cb)
      .catch(logoutOnError(commit));
  },
  [FETCH_LATTICE_NODES_BY_HEADWORD]: ({ commit }, { headword, lang }) => {
    const cb = (data) => commit(FETCH_LATTICE_NODES_BY_HEADWORD, data.data);
    return api.fetchLatticeNodes(headword, lang, cb).catch(logoutOnError(commit));
  },
  // TODO: might be a better way to reset this state but this works for now
  [RESET_LATTICE_NODES_BY_HEADWORD]: ({ commit }) => commit(RESET_LATTICE_NODES_BY_HEADWORD),
  [SET_LANGUAGE_PREF]: ({ commit }, { lang }) => {
    const cb = commit(SET_LANGUAGE_PREF, lang);
    return api.updateMeLang(lang, cb).catch(logoutOnError(commit));
  },
  [DELETE_PERSONAL_VOCAB_ENTRY]: ({ commit }, { id }) => {
    const cb = (data) => commit(DELETE_PERSONAL_VOCAB_ENTRY, data.data);
    return api.deletePersonalVocabEntry(id, cb)
      .catch(logoutOnError(commit));
  },
  [FETCH_BOOKMARKS]: ({ commit }) => (
    api
      .fetchBookmarks((data) => commit(FETCH_BOOKMARKS, data.data))
      .catch(logoutOnError(commit))
  ),
  [ADD_BOOKMARK]: ({ dispatch, commit }, { textId }) => (
    api
      .addBookmark(textId)
      .then(() => dispatch(FETCH_BOOKMARKS))
      .catch(logoutOnError(commit))
  ),
  [REMOVE_BOOKMARK]: ({ dispatch, commit }, { bookmarkId }) => (
    api
      .removeBookmark(bookmarkId)
      .then(() => dispatch(FETCH_BOOKMARKS))
      .catch(logoutOnError(commit))
  ),
  [FETCH_SUPPORTED_LANG_LIST]: ({ commit }) => (
    api.fetchSupportedLangList((data) => commit(FETCH_SUPPORTED_LANG_LIST, data.data))
      .catch(logoutOnError(commit))
  ),
  // TODO add suggested node functionality
  // [FETCH_LATTICE_NODES]: ({commit}, { headword }) => {
  //   const cb = (data) => commit(FETCH_LATTICE_NODES, data.data);
  //   return api.fetchLatticeNodes(headword, cb).catch(logoutOnError(commit));
  // }
};
