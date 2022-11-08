import { shallowMount, createLocalVue, mount } from '@vue/test-utils';
import Vuex from 'vuex';
import PersonalVocab from '../app/PersonalVocab.vue';
import testData from './testData';

const localVue = createLocalVue();
localVue.use(Vuex);

describe('PersonalVocab', () => {
  let actions;
  let store;
  const { personalVocabList, supportedLanguages } = testData;
  beforeEach(() => {
    actions = {
      fetchMe: jest.fn(),
      fetchPersonalVocabList: jest.fn(),
      deletePersonalVocabEntry: jest.fn(),
      fetchSupportedLangList: jest.fn(),
      fetchPersonalVocabLangList: jest.fn(),
    };

    store = new Vuex.Store({
      state: {
        personalVocabList,
        supportedLanguages,
        personalVocabLangList: [{ lang: 'lat', id: 67 }],
      },
      actions,
    });
  });
  it('loads in edit button PersonalVocab', () => {
    const wrapper = mount(PersonalVocab, { store, localVue });
    expect(wrapper.find('#td-edit-button').exists()).toBe(true);
  });

  it('loads in delete button PersonalVocab', async () => {
    const wrapper = mount(PersonalVocab, { store, localVue });
    await wrapper.find('#td-edit-button').trigger('click');
    expect(wrapper.find('#td-delete-button').exists()).toBe(true);
  });

  it('should not load delete button if edit button is not clicked', () => {
    store = new Vuex.Store({
      state: {
        personalVocabList: null,
      },
      actions,
    });
    const wrapper = shallowMount(PersonalVocab, { store, localVue });
    expect(wrapper.find('#td-delete-button').exists()).toBe(false);
  });
  it('should successfully delete a vocab from the list', async () => {
    // https://vue-test-utils.vuejs.org/api/options.html#stubs
    const wrapper = mount(PersonalVocab, {
      store,
      localVue,
      stubs: {
        QuickAddVocabForm: false,
      },
    });
    await wrapper.find('#td-edit-button').trigger('click');
    wrapper.find('#td-delete-button').trigger('click');
    expect(actions.deletePersonalVocabEntry).toHaveBeenCalled();
  });
});
