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
});