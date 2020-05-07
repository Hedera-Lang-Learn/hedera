import Vue from 'vue';
import Vuex from 'vuex';

import {
  actions, getters, mutations, state,
} from './vuex';

Vue.use(Vuex);

const debug = process.env.NODE_ENV !== 'production';

export default new Vuex.Store({
  state,
  actions,
  getters,
  mutations,
  strict: true,
  debug,
});
