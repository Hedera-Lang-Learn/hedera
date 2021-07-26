import { createLocalVue, mount } from '@vue/test-utils';
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
      fetchLatticeNodesByHeadword: jest.fn(),
      resetLatticeNodesByHeadword: jest.fn(),
      fetchMe: jest.fn(),
    };

    store = new Vuex.Store({
      state: {
        personalVocabLangList: [],
        latticeNodes: [],
      },
      actions,
    });
  });

  it('loads in QuickVocabForm', () => {
    const wrapper = mount(QuickVocabAddForm, { store, localVue });
    expect(wrapper.find('#addvocab-form').isVisible()).toBe(true);
  });

  // it('loads latticeNodes when data exist', () => {
  //   store.state.latticeNodes = {
  //     pk: 1,
  //     label: 'sum, esse, fuī',
  //     gloss: 'to be, exist',
  //     canonical: true,
  //     forms: [],
  //     lemmas: [{ lemma: 'sum', context: 'morpheus' }],
  //     vocabulary_entries: [],
  //     children: []
  //   };
  //   const wrapper = mount(QuickVocabAddForm, { store, localVue });
  // });

  it('fails to calls store createPersonalVocabEntry "submit" when button is clicked', () => {
    const wrapper = mount(QuickVocabAddForm, { store, localVue });
    wrapper.find("[type='submit']").trigger('click');
    expect(actions.createPersonalVocabEntry).toHaveBeenCalledTimes(0);
  });

  it('successfully calls store createPersonalVocabEntry "submit" when button is clicked', () => {
    store.state.personalVocabLangList = [
      {
        lang: 'lat',
        id: 1,
      },
      {
        lang: 'grc',
        id: 36,
      },
    ];
    const wrapper = mount(QuickVocabAddForm, { store, localVue });
    const options = wrapper.find('select').findAll('option');
    options.at(1).setSelected();
    wrapper.find('input[type=text][placeholder=headword]').setValue('sum');
    expect(actions.fetchLatticeNodesByHeadword).toHaveBeenCalled();
    wrapper.find('input[type=text][placeholder=gloss]').setValue('testGloss');
    wrapper.find("[type='submit']").trigger('click');
    expect(actions.createPersonalVocabEntry).toHaveBeenCalled();
  });
});
