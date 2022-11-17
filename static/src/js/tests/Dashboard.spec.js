import { shallowMount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import { FETCH_ME, FETCH_SUPPORTED_LANG_LIST } from '../app/constants';
import Dashboard from '../app/Dashboard.vue';

const localVue = createLocalVue();
localVue.use(Vuex);

describe('Dashboard', () => {
  let actions;
  let store;
  beforeEach(() => {
    actions = {
      [FETCH_ME]: jest.fn(),
      [FETCH_SUPPORTED_LANG_LIST]: jest.fn(),
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
