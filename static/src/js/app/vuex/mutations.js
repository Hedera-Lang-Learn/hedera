import {
  FETCH_TOKENS,
  SELECT_TOKEN,
  FETCH_NODE,
  FETCH_LEMMA,
  FETCH_LEMMAS_BY_FORM,
  UPDATE_TOKEN,
  SET_TEXT_ID,
  FETCH_VOCAB_LISTS,
  SET_VOCAB_LIST,
  TOGGLE_SHOW_IN_VOCAB_LIST,
  FETCH_TEXT,
  FETCH_PERSONAL_VOCAB_LIST,
  FETCH_ME,
  FETCH_PERSONAL_VOCAB_LANG_LIST,
  CREATE_PERSONAL_VOCAB_ENTRY,
  FETCH_LATTICE_NODES_BY_HEADWORD,
  RESET_LATTICE_NODES_BY_HEADWORD,
  SET_LANGUAGE_PREF,
  DELETE_PERSONAL_VOCAB_ENTRY,
  FETCH_BOOKMARKS,
  FETCH_SUPPORTED_LANG_LIST,
} from '../constants';

export default {
  [FETCH_ME]: (state, data) => {
    state.me = data;
  },
  [FETCH_TEXT]: (state, data) => {
    state.text = data;
  },
  [FETCH_VOCAB_LISTS]: (state, data) => {
    state.vocabLists = data;
  },
  [FETCH_PERSONAL_VOCAB_LIST]: (state, data) => {
    state.personalVocabList = data;
  },
  [SET_TEXT_ID]: (state, id) => {
    state.textId = id;
  },
  [FETCH_TOKENS]: (state, data) => {
    state.tokens = data;
  },
  [SELECT_TOKEN]: (state, { token, data }) => {
    state.selectedToken = token;
    state.selectedTokenHistory = data.data.tokenHistory;
  },
  [FETCH_NODE]: (state, data) => {
    state.nodes = {
      ...state.nodes,
      [data.pk]: data,
    };
  },
  [FETCH_LEMMA]: (state, data) => {
    const lemma = data.data;
    state.lemmas = {
      ...state.lemmas,
      [lemma.pk]: lemma,
    };
  },
  [FETCH_LEMMAS_BY_FORM]: (state, data) => {
    const form = data.data;
    state.forms = {
      ...state.forms,
      [form.form]: form,
    };
  },
  [UPDATE_TOKEN]: (state, data) => {
    state.tokens = data.tokens;
    state.selectedTokenHistory = data.tokenHistory;
    if (state.selectedToken) {
      state.selectedToken = state.tokens[state.selectedToken.tokenIndex];
    }
  },
  [SET_VOCAB_LIST]: (state, id) => {
    state.selectedVocabList = id;
  },
  [TOGGLE_SHOW_IN_VOCAB_LIST]: (state) => {
    state.showInVocabList = !state.showInVocabList;
  },
  [FETCH_PERSONAL_VOCAB_LANG_LIST]: (state, data) => {
    state.personalVocabLangList = data;
  },
  [CREATE_PERSONAL_VOCAB_ENTRY]: (state, data) => {
    state.personalVocabAdded = data.created;
    if (state.personalVocabList.entries) {
      state.personalVocabList.entries = [data.data, ...state.personalVocabList.entries];
    }
  },
  [FETCH_LATTICE_NODES_BY_HEADWORD]: (state, data) => {
    state.latticeNodes = data;
  },
  [RESET_LATTICE_NODES_BY_HEADWORD]: (state) => {
    state.latticeNodes = [];
  },
  [SET_LANGUAGE_PREF]: (state, data) => {
    state.me = data;
  },
  [DELETE_PERSONAL_VOCAB_ENTRY]: (state, data) => {
    const index = state.personalVocabList.entries.findIndex((vocab) => vocab.id === data.id);
    if (index >= 0) state.personalVocabList.entries.splice(index, 1);
  },
  [FETCH_BOOKMARKS]: (state, data) => {
    state.bookmarks = data;
  },
  [FETCH_SUPPORTED_LANG_LIST]: (state, data) => {
    state.supportedLanguages = data;
  },
};
