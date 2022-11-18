import { shallowMount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import { PROFILE_FETCH, SUPPORTED_LANG_LIST_FETCH } from '../app/constants';
import Dashboard from '../app/Dashboard.vue';

const localVue = createLocalVue();
localVue.use(Vuex);

describe('Dashboard', () => {
  let actions;
  let store;
  beforeEach(() => {
    actions = {
      [PROFILE_FETCH]: jest.fn(),
      [SUPPORTED_LANG_LIST_FETCH]: jest.fn(),
    };

    store = new Vuex.Store({
      // The tests get confused about something around here?
      // console.error
      //   [vuex] unknown action type: fetchSupportedLangList
      state: {},
      actions,
    });
  });
  it('loads in dashboard', () => {
    const wrapper = shallowMount(Dashboard, { store, localVue });
    expect(wrapper.classes('dashboard')).toBe(true);
  });
});
