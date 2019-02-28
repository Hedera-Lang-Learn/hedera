import { FETCH_TOKENS, SELECT_TOKEN, FETCH_NODE, UPDATE_TOKEN, SET_TEXT_ID, FETCH_VOCAB_LISTS, TOGGLE_VOCAB_LIST, TOGGLE_SHOW_IN_VOCAB_LIST } from '../constants';

export default {
  [FETCH_VOCAB_LISTS]: (state, data) => {
    state.vocabLists = data;
  },
  [SET_TEXT_ID]: (state, id) => {
    state.textId = id;
  },
  [FETCH_TOKENS]: (state, data) => {
    state.tokens = data;
  },
  [SELECT_TOKEN]: (state, { token, index }) => {
    state.selectedToken = token;
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
  [TOGGLE_VOCAB_LIST]: (state, id) => {
    if (state.selectedVocabList === id) {
      state.selectedVocabList = null;
    } else {
      state.selectedVocabList = id;
    }
  },
  [TOGGLE_SHOW_IN_VOCAB_LIST]: (state) => {
    state.showInVocabList = !state.showInVocabList;
  },
};
