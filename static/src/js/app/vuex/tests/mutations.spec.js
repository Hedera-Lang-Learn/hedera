import mutations from '../mutations';
import state from '../state';

describe('Mutations', () => {
  describe('fetchPersonalVocabLangList', () => {
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

      mutations.fetchPersonalVocabLangList(state, data);
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
      mutations.createPersonalVocabEntry(state, data);
      expect(state.personalVocabAdded).toBe(true);
      expect(state.personalVocabList.entries).toBe(undefined);
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

      mutations.createPersonalVocabEntry(updatedState, data);
      expect(updatedState.personalVocabAdded).toBe(true);
      expect(updatedState.personalVocabList.entries.length).toBe(2);
    });
  });

  describe('setLanguagePref', () => {
    it('successfully updates the state', () => {
      const data = {
        email: 'testing@test.com',
        displayName: 'vez-test',
        showNodeIds: 'toggle',
        lang: 'lat',
      };
      mutations.setLanguagePref(state, data);
      expect(state.me).toEqual(data);
    });
  });
  describe('deletePersonalVocabEntry', () => {
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
      mutations.deletePersonalVocabEntry(modifiedState, data);
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
      mutations.deletePersonalVocabEntry(modifiedState, data);
      expect(modifiedState.personalVocabList.entries.length).toBe(1);
    });
  });
});
