import { shallowMount, createLocalVue, mount } from '@vue/test-utils';
import Vuex from 'vuex';
import PersonalVocab from '../app/PersonalVocab.vue';

const localVue = createLocalVue();
localVue.use(Vuex);

describe('PersonalVocab', () => {
  let actions;
  let store;
  beforeEach(() => {
    actions = {
      fetchMe: jest.fn(),
      fetchPersonalVocabList: jest.fn(),
      deletePersonalVocabEntry: jest.fn(),
      fetchSupportedLangList: jest.fn(),
    };

    store = new Vuex.Store({
      state: {
        personalVocabList: {
          entries: [
            {
              familiarity: 1,
              gloss: 'large, spacious',
              headword: 'amplus -a -um',
              id: 1244,
              node: 515,
            },
          ],
        },
        supportedLanguages: [],
      },
      actions,
    });
  });
  it('loads in delete button PersonalVocab', () => {
    const wrapper = mount(PersonalVocab, { store, localVue });
    expect(wrapper.find('#td-delete-button').exists()).toBe(true);
  });

  it('should not load delete button if there are no personal vocab in state', () => {
    store = new Vuex.Store({
      state: {
        personalVocabList: null,
      },
      actions,
    });
    const wrapper = shallowMount(PersonalVocab, { store, localVue });
    expect(wrapper.find('#td-delete-button').exists()).toBe(false);
  });
  it('should successfully delete a vocab from the list', () => {
    const wrapper = mount(PersonalVocab, {
      store,
      localVue,
      stubs: {
        QuickAddVocabForm: false,
      },
    });
    wrapper.find('#td-delete-button').trigger('click');
    expect(actions.deletePersonalVocabEntry).toHaveBeenCalled();
  });
});
