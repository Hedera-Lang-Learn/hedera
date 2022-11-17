import { createLocalVue, mount } from '@vue/test-utils';
import Vuex from 'vuex';
import {
  DELETE_VOCAB_ENTRY,
  FETCH_ME,
  FETCH_PERSONAL_VOCAB_LANG_LIST,
  FETCH_SUPPORTED_LANG_LIST,
  FETCH_VOCAB_LIST,
  SET_VOCAB_LIST_TYPE,
  UPDATE_VOCAB_ENTRY,
} from '../app/constants';
import PersonalVocab from '../app/PersonalVocab.vue';
import testData from './testData';

const localVue = createLocalVue();
localVue.use(Vuex);

describe('VocabGeneral', () => {
  let actions;
  let store;
  const { supportedLanguages, generalVocabList } = testData;
  const state = {
    supportedLanguages,
    personalVocabLangList: [{ lang: 'lat', id: 67 }],
    vocabList: generalVocabList,
    vocabListType: 'general',
  };
  beforeEach(() => {
    actions = {
      [FETCH_ME]: jest.fn(),
      [FETCH_PERSONAL_VOCAB_LANG_LIST]: jest.fn(),
      [FETCH_SUPPORTED_LANG_LIST]: jest.fn(),
      [FETCH_VOCAB_LIST]: jest.fn(),
      [SET_VOCAB_LIST_TYPE]: jest.fn(),
      [UPDATE_VOCAB_ENTRY]: jest.fn(),
      [DELETE_VOCAB_ENTRY]: jest.fn(),
    };

    store = new Vuex.Store({
      state,
      actions,
    });
  });

  it('loads in edit button Vocab - general', () => {
    const wrapper = mount(PersonalVocab, { store, localVue });
    expect(wrapper.find('#td-edit-button').exists()).toBe(true);
  });

  it('does not load in edit button Vocab when general list is not editable', () => {
    // set vocab list edit permission to false, then set back true after test
    store.state.vocabList.canEdit = false;
    const wrapper = mount(PersonalVocab, { store, localVue });
    expect(wrapper.find('#td-edit-button').exists()).toBe(false);
    store.state.vocabList.canEdit = true;
  });

  it('edits a vocab entry when save is clicked', async () => {
    const wrapper = mount(PersonalVocab, { store, localVue });
    await wrapper.find('#td-edit-button').trigger('click');
    await wrapper.find('#td-save-button').trigger('click');
    expect(actions[UPDATE_VOCAB_ENTRY]).toHaveBeenCalled();
  });

  it('loads in delete button Vocab - general', async () => {
    const wrapper = mount(PersonalVocab, { store, localVue });
    await wrapper.find('#td-edit-button').trigger('click');
    expect(wrapper.find('#td-delete-button').exists()).toBe(true);
  });

  it('should not load delete button if edit button is not clicked', () => {
    const wrapper = mount(PersonalVocab, { store, localVue });
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
    expect(actions[DELETE_VOCAB_ENTRY]).toHaveBeenCalled();
  });
});
