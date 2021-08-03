import mutations from '../mutations';

describe('Mutations', () => {
  describe('fetchPersonalVocabLangList', () => {
    it('successfully updates state', () => {
      const state = {
        personalVocabLangList: null,
      };
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
    it('successfully updates the state', () => {
      const state = {
        personalVocabAdded: false,
      };
      const data = { created: true };
      mutations.createPersonalVocabEntry(state, data);
      expect(state.personalVocabAdded).toBe(true);
    });
  });

  describe('deletePersonalVocabEntry', () => {
    it('successfully updates the state', () => {
      const state = {
        personalVocabList: {
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
      mutations.deletePersonalVocabEntry(state, data);
      expect(state.personalVocabList.entries.length).toBe(0);
    });
    it('unsuccessfully updates the state', () => {
      const state = {
        personalVocabList: {
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
      mutations.deletePersonalVocabEntry(state, data);
      expect(state.personalVocabList.entries.length).toBe(1);
    });
  });
});
