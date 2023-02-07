import axios from 'axios';
import {
  PROFILE_FETCH,
  PERSONAL_VOCAB_ENTRY_CREATE,
  PERSONAL_VOCAB_ENTRY_DELETE,
  PERSONAL_VOCAB_LIST_FETCH_LANG_LIST,
  PROFILE_SET_LANGUAGE_PREF,
} from '../../constants';
import actions from '../actions';

const BASE_URL = '/api/v1/';

jest.mock('axios');

describe('Actions', () => {
  /* This is a reference implementation for testing vuex actions, so it has
  more comments than usual. The basic idea is to test that whatever API calls
  the function uses get called with expected parameters, and that the resulting
  call to the mutation gets called with its own expected parameters. The test
  doesn't rely on a functioning api endpoint; instead jest is mocking axios
  calls, and each test is using axios.<method>.mockResolvedValueOnce(response),
  where `response` is an object that has the keys of an axios response that the
  function expects. Note that the body of a response is in the `data` key of an
  axios response, so most API calls will make use of that key. Reference the
  axios response schema for other parts of the response that may be used.

  Ideally tests should be grouped by data models, similar to the way that the
  actions themselves are grouped, and each `describe()` should include some
  shared objects for expected payloads and responses. Unfortunately
  idiosyncracies in how the Django API is constructed make this impractical in
  many cases, but it's something to shoot for. */
  describe('hedera.Profile', () => {
    const profile = {
      data: { // axios data wrapper
        data: { // api response data wrapper
          displayName: 'mockUser',
          email: 'mock@mock.mock',
          lang: 'lat',
          showNodeIds: 'never',
        },
      },
    };

    it(`${PROFILE_FETCH} handles successful api response`, async () => {
      // mock response from API, retrieved via axios
      axios.get.mockResolvedValueOnce(profile);

      // mock the commit
      const commit = jest.fn();
      await actions[PROFILE_FETCH]({ commit });

      // expect the API to have been called with the appropriate URL
      expect(axios.get).toHaveBeenCalledWith(`${BASE_URL}me/`);

      // expect the correct mutation to have been called with the correct update data
      expect(commit).toHaveBeenCalledWith(
        PROFILE_FETCH,
        profile.data.data,
      );
    });

    it(`${PROFILE_SET_LANGUAGE_PREF} handles successful api response`, async () => {
      axios.post.mockResolvedValueOnce(profile);
      const payload = { lang: 'lat' };
      const commit = jest.fn();
      await actions[PROFILE_SET_LANGUAGE_PREF]({ commit }, payload);
      expect(axios.post).toHaveBeenCalledWith(`${BASE_URL}me/`, payload);
      expect(commit).toHaveBeenCalledWith(
        PROFILE_SET_LANGUAGE_PREF,
        profile.data.data.lang,
      );
    });
  });
  describe('vocab_list.PersonalVocabularyList', () => {
    const apiResponse = {
      data: {
        data: [
          { lang: 'lat', id: 1 },
        ],
      },
    };

    it(`${PERSONAL_VOCAB_LIST_FETCH_LANG_LIST} handles successful api response`, async () => {
      axios.get.mockResolvedValueOnce(apiResponse);
      const commit = jest.fn();
      await actions[PERSONAL_VOCAB_LIST_FETCH_LANG_LIST]({ commit });
      expect(axios.get).toHaveBeenCalledWith(`${BASE_URL}personal_vocab_list/quick_add/`);
      expect(commit).toHaveBeenCalledWith(
        PERSONAL_VOCAB_LIST_FETCH_LANG_LIST,
        apiResponse.data.data,
      );
    });
  });

  describe('vocab_list.PersonalVocabularyEntry', () => {
    it(`${PERSONAL_VOCAB_ENTRY_CREATE} works with well-formed payload`, async () => {
      const commit = jest.fn();
      // payload sent to action
      const payload = {
        headword: 'ergo',
        definition: 'sum',
        lemmaId: 1,
        familiarity: 1,
        lang: 'lat',
        vocabularyListId: 1,
      };
      // payload sent to api function
      const { lemmaId, vocabularyListId, ...apiPayload } = payload;
      apiPayload.lemma_id = lemmaId;
      apiPayload.vocabulary_list_id = vocabularyListId;
      // mocked API response
      const apiResponse = {
        data: {
          data: {
            created: true,
            data: {},
          },
        },
      };
      axios.post.mockResolvedValueOnce(apiResponse);
      await actions[PERSONAL_VOCAB_ENTRY_CREATE]({ commit }, payload);
      expect(axios.post).toHaveBeenCalledWith(
        `${BASE_URL}personal_vocab_list/quick_add/`,
        apiPayload,
      );
      expect(commit).toHaveBeenCalledWith(
        PERSONAL_VOCAB_ENTRY_CREATE,
        apiResponse.data.data,
      );
    });

    it(`${PERSONAL_VOCAB_ENTRY_DELETE} works with well-formed payload`, async () => {
      const vocabEntryId = 1;
      const payload = { id: vocabEntryId };
      const commit = jest.fn();
      const apiResponse = {
        data: {
          data: true,
          id: vocabEntryId,
        },
      };
      axios.delete.mockResolvedValueOnce(apiResponse);
      await actions[PERSONAL_VOCAB_ENTRY_DELETE]({ commit }, payload);
      expect(axios.delete).toHaveBeenCalledWith(
        `${BASE_URL}personal_vocab_list/`,
        { data: { id: payload.id } },
      );
      expect(commit).toHaveBeenCalledWith(
        PERSONAL_VOCAB_ENTRY_DELETE,
        apiResponse.data,
      );
    });
  });
});
