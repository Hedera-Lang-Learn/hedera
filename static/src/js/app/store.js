import Vue from 'vue';
import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate';

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
  plugins: [
    createPersistedState({
      paths: [
        'sidebarLeftOpened',
        'sidebarRightOpened',
      ],
      storage: window.localStorage,
    }),
  ],
});
