import { shallowMount, createLocalVue } from '@vue/test-utils';
import Vuex from 'vuex';
import QuickVocabAddForm from '../app/components/quick-add-button/QuickAddButton.vue';

const localVue = createLocalVue();
localVue.use(Vuex);

describe('QuickVocabForm', () => {
  let actions;
  let store;
  beforeEach(() => {
    actions = {
      fetchPersonalVocabLangList: jest.fn(),
      createPersonalVocabEntry: jest.fn(),
    };

    store = new Vuex.Store({
      state: {
        personalVocabLangList: [
          {
            lang: 'lat',
            id: 1,
          },
          {
            lang: 'grc',
            id: 36,
          },
        ],
      },
      actions,
    });
  });
  it('loads in QuickVocabForm', () => {
    const wrapper = shallowMount(QuickVocabAddForm, { store, localVue });
    expect(wrapper.find('#addvocab-form').exists()).toBe(true);
  });
  it('successfully calls store createPersonalVocabEntry "submit" when button is clicked', async () => {
    const wrapper = shallowMount(QuickVocabAddForm, { store, localVue });
    await wrapper.find('select').setValue(1);
    await wrapper
      .find('input[type=text][placeholder=headword]')
      .setValue('testHeadword');
    await wrapper
      .find('input[type=text][placeholder=gloss]')
      .setValue('testGloss');
    wrapper.find('form').trigger('submit.prevent');
    expect(actions.createPersonalVocabEntry).toHaveBeenCalled();
  });
});
