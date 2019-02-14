import { FETCH_ITEMS, SELECT_TOKEN } from '../constants';

export default {
  [FETCH_ITEMS]: (state, data) => {
    state.texts = data;
  },
  [SELECT_TOKEN]: (state, { token, index }) => {
    state.selectedToken = token;
    state.selectedIndex = index;
  },
};
