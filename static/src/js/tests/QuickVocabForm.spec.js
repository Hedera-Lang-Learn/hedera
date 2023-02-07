import { createLocalVue, mount } from '@vue/test-utils';
import Vue from 'vue';
import Vuex from 'vuex';
import QuickVocabAddForm from '../app/components/quick-add-button/QuickAddButton.vue';
import {
  VOCAB_ENTRY_CREATE,
  LEMMA_FETCH,
  FORMS_FETCH,
  PROFILE_FETCH,
  PERSONAL_VOCAB_LIST_FETCH_LANG_LIST,
  SUPPORTED_LANG_LIST_FETCH,
  PROFILE_SET_LANGUAGE_PREF,
} from '../app/constants';
import testData from './testData';

const localVue = createLocalVue();
localVue.use(Vuex);

describe('QuickVocabForm', () => {
  let store;
  const actions = {
    [PERSONAL_VOCAB_LIST_FETCH_LANG_LIST]: jest.fn(),
    [VOCAB_ENTRY_CREATE]: jest.fn(),
    [FORMS_FETCH]: jest.fn(),
    [PROFILE_FETCH]: jest.fn(),
    [PROFILE_SET_LANGUAGE_PREF]: jest.fn(),
    [SUPPORTED_LANG_LIST_FETCH]: jest.fn(),
    [LEMMA_FETCH]: jest.fn(),
  };
  const state = {
    personalVocabLangList: [
      { lang: 'lat', id: 1 },
      { lang: 'grc', id: 36 },
    ],
    me: {
      email: 'testing@test.com',
      displayName: 'vez-test',
      showNodeIds: 'toggle',
      lang: 'lat',
    },
    supportedLanguages: testData.supportedLanguages,
  };
  beforeEach(() => {
    store = new Vuex.Store({
      state,
      actions,
    });
  });

  it('loads in QuickVocabForm', () => {
    const wrapper = mount(QuickVocabAddForm, { store, localVue });
    expect(wrapper.find('#addvocab-form').isVisible()).toBe(true);
  });

  it('loads lemma options when data exist', async () => {
    const { forms } = testData;
    const newState = {
      lemmas: forms.sum.lemmas,
      forms,
      ...state,
    };
    store = new Vuex.Store({
      state: newState,
      actions,
    });
    const wrapper = await mount(QuickVocabAddForm, {
      store,
      localVue,
    });
    // Enter a headword so that options appear
    await wrapper.find('#quick-add-form-headword-entry').setValue(forms.sum.form);
    const lemmaInputs = wrapper.find('#lemma-options-inputs').findAll('input');
    // Note: for debugging an array of options - wrapper.find('#FormControlSelect').findAll('option').wrappers.forEach(w=>console.log(w.html()))
    await lemmaInputs.at(0).setChecked();
    await wrapper
      .find('input[type=text][placeholder=headword]')
      .setValue('sum');
    await Vue.nextTick();
    expect(
      wrapper.find(`#lemma-option-${forms.sum.lemmas[0].pk}`).exists(),
    ).toBe(true);
  });

  it('should not load suggested lemmas when data does not exist', () => {
    const wrapper = mount(QuickVocabAddForm, { store, localVue });
    expect(wrapper.findAll('lemma-label')).toHaveLength(0);
  });

  it('fails to calls store createVocabEntry "submit" when button is clicked', () => {
    const wrapper = mount(QuickVocabAddForm, { store, localVue });
    wrapper.find("[type='submit']").trigger('click');
    expect(actions[VOCAB_ENTRY_CREATE]).toHaveBeenCalledTimes(0);
  });

  it('successfully calls store createVocabEntry "submit" when button is clicked', async () => {
    const { forms, personalVocabList } = testData;
    const newState = {
      lemmas: forms.sum.lemmas,
      forms,
      vocabList: personalVocabList,
      ...state,
    };
    store = new Vuex.Store({
      state: newState,
      actions,
    });
    const wrapper = mount(QuickVocabAddForm, {
      store,
      localVue,
    });
    // Enter a headword so that options appear
    await wrapper
      .find('input[type=text][placeholder=headword]')
      .setValue(forms.sum.form);
    const lemmaInputs = wrapper.find('#lemma-options-inputs').findAll('input');
    await lemmaInputs.at(0).setChecked();
    await wrapper
      .find('input[type=text][placeholder=definition]')
      .setValue('testGloss');
    await Vue.nextTick();
    await wrapper.find("[type='submit']").trigger('click');
    expect(actions[VOCAB_ENTRY_CREATE]).toHaveBeenCalled();
  });
});
