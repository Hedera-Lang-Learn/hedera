import { createLocalVue, mount } from '@vue/test-utils';
import Vuex from 'vuex';
import PersonalVocab from '../app/PersonalVocab.vue';
import testData from './testData';

const localVue = createLocalVue();
localVue.use(Vuex);

describe('VocabPersonal', () => {
  let actions;
  let propsData;
  let store;
  const { supportedLanguages, personalVocabList } = testData;
  const state = {
    supportedLanguages,
    personalVocabLangList: [{ lang: 'lat', id: 67 }],
    vocabList: personalVocabList,
    vocabListType: 'personal',
  };
  beforeEach(() => {
    actions = {
      deletePersonalVocabEntry: jest.fn(),
      fetchMe: jest.fn(),
      fetchPersonalVocabLangList: jest.fn(),
      fetchPersonalVocabList: jest.fn(),
      fetchSupportedLangList: jest.fn(),
      fetchVocabList: jest.fn(),
      setVocabListType: jest.fn(),
      updatePersonalVocabEntry: jest.fn(),
      vocabEntryDelete: jest.fn(),
    };

    propsData = {
      vocabId: 0,
      lang: 'lat',
      personalVocab: true,
    }

    store = new Vuex.Store({
      state,
      actions,
    });
  });

  it('loads in edit button Vocab - personal', () => {
    const wrapper = mount(PersonalVocab, { propsData, store, localVue });
    expect(wrapper.find('#td-edit-button').exists()).toBe(true);
  });

  it('edits a vocab entry when save is clicked', async () => {
    const wrapper = mount(PersonalVocab, { propsData, store, localVue });
    await wrapper.find("#td-edit-button").trigger('click');
    await wrapper.find("#td-save-button").trigger('click');
    expect(actions.updatePersonalVocabEntry).toHaveBeenCalled();
  });

  it('loads in delete button Vocab - personal', async () => {
    const wrapper = mount(PersonalVocab, { propsData, store, localVue });
    await wrapper.find('#td-edit-button').trigger('click');
    expect(wrapper.find('#td-delete-button').exists()).toBe(true);
  });

  it('should not load delete button if edit button is not clicked', () => {
    const wrapper = mount(PersonalVocab, { propsData, store, localVue });
    expect(wrapper.find('#td-delete-button').exists()).toBe(false);
  });

  it('should successfully delete a vocab from the list', async () => {
    // https://vue-test-utils.vuejs.org/api/options.html#stubs
    const wrapper = mount(PersonalVocab, {
      propsData,
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
