import { createLocalVue, mount } from '@vue/test-utils';
import Vuex from 'vuex';
import {
  DELETE_PERSONAL_VOCAB_ENTRY,
  FETCH_ME,
  FETCH_PERSONAL_VOCAB_LANG_LIST,
  FETCH_PERSONAL_VOCAB_LIST,
  FETCH_SUPPORTED_LANG_LIST,
  SET_VOCAB_LIST_TYPE,
  UPDATE_PERSONAL_VOCAB_ENTRY,
} from '../app/constants';
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
      [DELETE_PERSONAL_VOCAB_ENTRY]: jest.fn(),
      [FETCH_ME]: jest.fn(),
      [FETCH_PERSONAL_VOCAB_LANG_LIST]: jest.fn(),
      [FETCH_PERSONAL_VOCAB_LIST]: jest.fn(),
      [FETCH_SUPPORTED_LANG_LIST]: jest.fn(),
      [SET_VOCAB_LIST_TYPE]: jest.fn(),
      [UPDATE_PERSONAL_VOCAB_ENTRY]: jest.fn(),
    };

    propsData = {
      vocabId: 0,
      lang: 'lat',
      personalVocab: true,
    };

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
    await wrapper.find('#td-edit-button').trigger('click');
    await wrapper.find('#td-save-button').trigger('click');
    expect(actions[UPDATE_PERSONAL_VOCAB_ENTRY]).toHaveBeenCalled();
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
    expect(actions[DELETE_PERSONAL_VOCAB_ENTRY]).toHaveBeenCalled();
  });
});
