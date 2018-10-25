import { TOGGLE_SIDEBAR_LEFT, TOGGLE_SIDEBAR_RIGHT } from '../constants';

export default {
  [TOGGLE_SIDEBAR_LEFT]: ({ commit }) => commit(TOGGLE_SIDEBAR_LEFT),
  [TOGGLE_SIDEBAR_RIGHT]: ({ commit }) => commit(TOGGLE_SIDEBAR_RIGHT),
};
