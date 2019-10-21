import {
  FETCH_TOKENS,
  SELECT_TOKEN,
  FETCH_NODE,
  UPDATE_TOKEN,
  SET_TEXT_ID,
  FETCH_VOCAB_LISTS,
  SET_VOCAB_LIST,
  TOGGLE_SHOW_IN_VOCAB_LIST,
  FETCH_TEXT,
  FETCH_PERSONAL_VOCAB_LIST,
} from '../constants';

export default {
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
  [SELECT_TOKEN]: (state, { index }) => {
    state.selectedIndex = index;
  },
  [FETCH_NODE]: (state, data) => {
    state.nodes = {
      ...state.nodes,
      [data.pk]: data,
    };
  },
  [UPDATE_TOKEN]: (state, data) => {
    state.tokens = data;
    state.selectedToken = state.tokens[state.selectedIndex];
  },
  [SET_VOCAB_LIST]: (state, id) => {
    state.selectedVocabList = id;
  },
  [TOGGLE_SHOW_IN_VOCAB_LIST]: (state) => {
    state.showInVocabList = !state.showInVocabList;
  },
};
