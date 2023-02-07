import {
  PERSONAL_VOCAB_ENTRY_CREATE,
  PERSONAL_VOCAB_ENTRY_DELETE,
  PERSONAL_VOCAB_LIST_FETCH_LANG_LIST,
  PROFILE_SET_LANGUAGE_PREF,
} from '../../constants';
import mutations from '../mutations';
import state from '../state';

describe('Mutations', () => {
  describe('PERSONAL_VOCAB_LIST_FETCH_LANG_LIST', () => {
    it('successfully updates state', () => {
      const data = [
        {
          lang: 'lat',
          id: 1,
        },
        {
          lang: 'grc',
          id: 36,
        },
      ];

      mutations[PERSONAL_VOCAB_LIST_FETCH_LANG_LIST](state, data);
      expect(state.personalVocabLangList).toBe(data);
    });
  });

  describe('createPersonalVocab', () => {
    const vocabData = {
      id: 19,
      headword: 'foo',
      gloss: 'bar',
      familiarity: 1,
      node: null,
    };
    const data = {
      created: true,
      data: vocabData,
    };

    it('successfully updates the state without entries fetched', () => {
      mutations[PERSONAL_VOCAB_ENTRY_CREATE](state, data);
      expect(state.vocabAdded).toBe(true);
      expect(state.vocabList.entries).toBe(undefined);
    });

    it('successfully updates the state with entries fetched', () => {
      const updatedState = {
        ...state,
        personalVocabList: {
          ...state.personalVocabList,
          entries: [
            {
              id: 1,
              headword: 'test',
              gloss: 'tes',
              familiarity: 1,
              node: null,
            },
          ],
        },
      };

      mutations[PERSONAL_VOCAB_ENTRY_CREATE](updatedState, data);
      expect(updatedState.vocabAdded).toBe(true);
      expect(updatedState.personalVocabList.entries.length).toBe(2);
    });
  });

  describe('PROFILE_SET_LANGUAGE_PREF', () => {
    it('successfully updates the state', () => {
      const data = {
        email: 'testing@test.com',
        displayName: 'vez-test',
        showNodeIds: 'toggle',
        lang: 'lat',
      };
      mutations[PROFILE_SET_LANGUAGE_PREF](state, data);
      expect(state.me).toEqual(data);
    });
  });
  describe('PERSONAL_VOCAB_ENTRY_DELETE', () => {
    it('successfully updates the state', () => {
      const modifiedState = {
        ...state,
        personalVocabList: {
          ...state.personalVocabList,
          entries: [
            {
              id: 1,
              headword: 'amplus -a -um',
              gloss: 'large, spacious',
              familiarity: 1,
              node: 515,
            },
          ],
        },
      };
      const data = { data: true, id: 1 };
      mutations[PERSONAL_VOCAB_ENTRY_DELETE](modifiedState, data);
      expect(modifiedState.personalVocabList.entries.length).toBe(0);
    });
    it('unsuccessfully updates the state', () => {
      const modifiedState = {
        ...state,
        personalVocabList: {
          ...state.personalVocabList,
          entries: [
            {
              id: 1,
              headword: 'amplus -a -um',
              gloss: 'large, spacious',
              familiarity: 1,
              node: 515,
            },
          ],
        },
      };
      const data = { data: true, id: 11 };
      mutations[PERSONAL_VOCAB_ENTRY_DELETE](modifiedState, data);
      expect(modifiedState.personalVocabList.entries.length).toBe(1);
    });
  });
});
