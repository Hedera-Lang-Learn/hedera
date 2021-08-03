import actions from '../actions';

let url = '';
let body = {};

jest.mock('axios', () => ({
  post: (_url, _body) => new Promise((resolve) => {
    url = _url;
    body = _body;
    resolve(true);
  }),
  get: (_url) => new Promise((resolve) => {
    url = _url;
    resolve(true);
  }),
  delete: (_url, _body) => new Promise((resolve) => {
    url = _url;
    body = _body;
    resolve(_body);
  }),
  defaults: { withCredentials: true },
}));
describe('Actions', () => {
  describe('FETCH_PERSONAL_VOCAB_LANG_LIST', () => {
    it('successfully calls fetchPersonalVocabLangList action to update state', async () => {
      const commit = jest.fn();
      // TODO: when passed in the response isnt returned from the commit in the expect block, check why
      //   const response = {
      //     data: [
      //       {
      //         lang: 'lat',
      //         id: 1
      //       },
      //       {
      //         lang: 'grc',
      //         id: 36
      //       }
      //     ]
      //   };
      await actions.fetchPersonalVocabLangList({ commit });
      expect(url).toBe('/api/v1/personal_vocab_list/quick_add/');
    //   expect(commit).toHaveBeenCalledWith(
    //     'fetchPersonalVocabLangList',
    //     undefined
    //   );
    });
  });
  describe('CREATE_PERSONAL_VOCAB_ENTRY', () => {
    it('successfully calls createPersonalVocabEntry action to update state', async () => {
      const commit = jest.fn();
      const payload = {
        headword: 'ergo',
        gloss: 'sum',
        vocabularyListId: 1,
        familiarity: 1,
      };
      //   const response = { data: { created: true } };
      await actions.createPersonalVocabEntry({ commit }, payload);
      // expect(commit).toHaveBeenCalledWith('createPersonalVocabEntry', response)
      expect(url).toBe('/api/v1/personal_vocab_list/quick_add/');
      expect(body).toEqual({
        headword: 'ergo',
        gloss: 'sum',
        vocabulary_list_id: 1,
        familiarity: 1,
      });
    });
  });

  describe('DELETE_PERSONAL_VOCAB_ENTRY', () => {
    it('successfully calls deletePersonalVocabEntry', async () => {
      const commit = jest.fn();
      const payload = { id: 1 };
      await actions.deletePersonalVocabEntry({ commit }, payload);
      expect(commit).toHaveBeenCalledWith('deletePersonalVocabEntry', payload);
      expect(body.data).toEqual(payload);
    });
  });
});
