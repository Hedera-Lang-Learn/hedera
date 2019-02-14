import { FETCH_TOKENS, SELECT_TOKEN, FETCH_NODE, UPDATE_TOKEN } from '../constants';

export default {
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
};
