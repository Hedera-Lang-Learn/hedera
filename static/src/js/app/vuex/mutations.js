import { FETCH_ITEMS, SELECT_TOKEN, FETCH_NODE, UPDATE_TOKEN } from '../constants';

export default {
  [FETCH_ITEMS]: (state, data) => {
    state.texts = data;
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
    state.texts = data;
    state.selectedToken = state.texts[state.selectedIndex];
  },
};
