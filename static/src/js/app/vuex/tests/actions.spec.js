import {
  PERSONAL_VOCAB_ENTRY_CREATE,
  PERSONAL_VOCAB_ENTRY_DELETE,
  PERSONAL_VOCAB_LIST_FETCH_LANG_LIST,
  PROFILE_SET_LANGUAGE_PREF,
} from '../../constants';
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
  describe('PERSONAL_VOCAB_LIST_FETCH_LANG_LIST', () => {
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
      await actions[PERSONAL_VOCAB_LIST_FETCH_LANG_LIST]({ commit });
      expect(url).toBe('/api/v1/personal_vocab_list/quick_add/');
    //   expect(commit).toHaveBeenCalledWith(
    //     PERSONAL_VOCAB_LIST_FETCH_LANG_LIST,
    //     undefined
    //   );
    });
  });
  describe('PERSONAL_VOCAB_ENTRY_CREATE', () => {
    it('successfully calls createPersonalVocabEntry action to update state', async () => {
      const commit = jest.fn();
      const payload = {
        headword: 'ergo',
        definition: 'sum',
        lemmaId: 1,
        familiarity: 1,
        lang: 'lat',
        vocabularyListId: 1,
      };
      //   const response = { data: { created: true } };
      await actions[PERSONAL_VOCAB_ENTRY_CREATE]({ commit }, payload);
      // expect(commit).toHaveBeenCalledWith(PERSONAL_VOCAB_ENTRY_CREATE, response)
      expect(url).toBe('/api/v1/personal_vocab_list/quick_add/');
      expect(body).toEqual({
        headword: 'ergo',
        definition: 'sum',
        vocabulary_list_id: 1,
        familiarity: 1,
        lemma_id: 1,
        lang: 'lat',
      });
    });
  });

  describe('PROFILE_SET_LANGUAGE_PREF', () => {
    it('successfully calls PROFILE_SET_LANGUAGE_PREF', async () => {
      const commit = jest.fn();
      const payload = {
        lang: 'lat',
      };
      await actions[PROFILE_SET_LANGUAGE_PREF]({ commit }, payload);
      expect(commit).toHaveBeenCalledWith(PROFILE_SET_LANGUAGE_PREF, 'lat');
    });
  });
  describe('PERSONAL_VOCAB_ENTRY_DELETE', () => {
    it('successfully calls PERSONAL_VOCAB_ENTRY_DELETE', async () => {
      const commit = jest.fn();
      const payload = { id: 1 };
      await actions[PERSONAL_VOCAB_ENTRY_DELETE]({ commit }, payload);
      expect(commit).toHaveBeenCalledWith(PERSONAL_VOCAB_ENTRY_DELETE, payload);
      expect(body.data).toEqual(payload);
    });
  });
});
