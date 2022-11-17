/* eslint-disable object-curly-newline */
import {
  FETCH_TEXT,
  FETCH_TOKENS,
  SELECT_TOKEN,
  FETCH_NODE,
  FETCH_LEMMA,
  FETCH_LEMMAS_BY_FORM,
  FETCH_LEMMAS_BY_PARTIAL_FORM,
  UPDATE_TOKEN,
  SET_TEXT_ID,
  FETCH_VOCAB_LISTS,
  SET_VOCAB_LIST,
  TOGGLE_SHOW_IN_VOCAB_LIST,
  FETCH_PERSONAL_VOCAB_LIST,
  OLD_CREATE_VOCAB_ENTRY,
  UPDATE_VOCAB_ENTRY,
  UPDATE_PERSONAL_VOCAB_ENTRY,
  FETCH_ME,
  FETCH_PERSONAL_VOCAB_LANG_LIST,
  CREATE_PERSONAL_VOCAB_ENTRY,
  SET_LANGUAGE_PREF,
  DELETE_PERSONAL_VOCAB_ENTRY,
  DELETE_VOCAB_ENTRY,
  FETCH_BOOKMARKS,
  ADD_BOOKMARK,
  REMOVE_BOOKMARK,
  FETCH_SUPPORTED_LANG_LIST,
  FETCH_VOCAB_LIST,
  SET_VOCAB_LIST_TYPE,
  CREATE_VOCAB_ENTRY,
  UPDATE_VOCAB_LIST,
  UPDATE_VOCAB_LIST_ENTRIES,
} from '../constants';
import api from '../api';

// eslint-disable-next-line no-unused-vars
const logoutOnError = (commit) => (error) => {
  if (error.response && error.response.status === 401) {
    window.location = '/';
  }
};

export default {
  /* -------------------------------------------------------------------------- */
  /*                               hedera.Profile                               */
  /* -------------------------------------------------------------------------- */
  [FETCH_ME]: ({ commit }) => api.fetchMe((data) => commit(FETCH_ME, data.data)),
  [SET_LANGUAGE_PREF]: ({ commit }, { lang }) => {
    const cb = commit(SET_LANGUAGE_PREF, lang);
    return api.updateMeLang(lang, cb).catch(logoutOnError(commit));
  },

  /* -------------------------------------------------------------------------- */
  /*                             lemmatization.Form                             */
  /* -------------------------------------------------------------------------- */
  [FETCH_LEMMAS_BY_FORM]: ({ commit }, { lang, form }) => api.fetchLemmasByForm(lang, form, (data) => commit(FETCH_LEMMAS_BY_FORM, data)),
  // Note: might be slow to looks up partial matches
  [FETCH_LEMMAS_BY_PARTIAL_FORM]: ({ commit }, { lang, form }) => api.fetchLemmasByPartialForm(lang, form, (data) => commit(FETCH_LEMMAS_BY_PARTIAL_FORM, data)),

  /* -------------------------------------------------------------------------- */
  /*                             lemmatization.Lemma                            */
  /* -------------------------------------------------------------------------- */
  [FETCH_LEMMA]: ({ commit }, { id }) => api.fetchLemma(id, (data) => commit(FETCH_LEMMA, data)),

  /* -------------------------------------------------------------------------- */
  /*                       lemmatized_text.LemmatizedText                       */
  /* -------------------------------------------------------------------------- */
  [FETCH_TEXT]: ({ commit }, { id }) => api
    .fetchText(id, (data) => commit(FETCH_TEXT, data.data))
    .catch(logoutOnError(commit)),
  [FETCH_TOKENS]: ({ commit }, { id, vocabListId, personalVocabListId }) => {
    commit(SET_TEXT_ID, id);
    const cb = (data) => commit(FETCH_TOKENS, data.data);
    return api
      .fetchTokens(id, vocabListId, personalVocabListId, cb)
      .catch(logoutOnError(commit));
  },
  [SELECT_TOKEN]: ({ commit, state }, { token }) => api.fetchTokenHistory(
    state.textId,
    token.tokenIndex,
    (data) => commit(SELECT_TOKEN, { token, data }),
  ),
  [UPDATE_TOKEN]: ({ commit, state }, { id, tokenIndex, lemmaId, glossIds, resolved }) => {
    // Fetch the most recent lemma data
    api
      .fetchLemma(lemmaId, (data) => commit(FETCH_LEMMA, data))
      .catch(logoutOnError(commit));

    // Callback to commit the changes once the API call has completed
    const mutate = (data) => commit(UPDATE_TOKEN, data.data);

    // Perform the API request to update the token data
    return api
      .updateToken(id, tokenIndex, resolved, state.selectedVocabList, lemmaId, glossIds, null, mutate)
      .catch(logoutOnError(commit));
  },

  /* -------------------------------------------------------------------------- */
  /*                   lemmatized_text.LemmatizedTextBookmark                   */
  /* -------------------------------------------------------------------------- */
  [FETCH_BOOKMARKS]: ({ commit }) => (
    api
      .fetchBookmarks((data) => commit(FETCH_BOOKMARKS, data.data))
      .catch(logoutOnError(commit))
  ),
  [ADD_BOOKMARK]: ({ dispatch, commit }, { textId }) => (
    api
      .addBookmark(textId)
      .then(() => dispatch(FETCH_BOOKMARKS))
      .catch(logoutOnError(commit))
  ),
  [REMOVE_BOOKMARK]: ({ dispatch, commit }, { bookmarkId }) => (
    api
      .removeBookmark(bookmarkId)
      .then(() => dispatch(FETCH_BOOKMARKS))
      .catch(logoutOnError(commit))
  ),

  /* -------------------------------------------------------------------------- */
  /*                      vocab_list.PersonalVocabularyList                     */
  /* -------------------------------------------------------------------------- */
  [FETCH_PERSONAL_VOCAB_LIST]: async ({ commit }, { lang }) => {
    const { data } = await api
      .fetchPersonalVocabList(lang)
      .catch(logoutOnError(commit));
    commit(UPDATE_VOCAB_LIST, data.data.personalVocabList);
  },
  [FETCH_PERSONAL_VOCAB_LANG_LIST]: ({ commit }) => {
    const cb = (data) => commit(FETCH_PERSONAL_VOCAB_LANG_LIST, data.data);
    return api
      .fetchPersonalVocabLangList(cb)
      .catch(logoutOnError(commit));
  },

  /* -------------------------------------------------------------------------- */
  /*                   vocab_list.PersonalVocabularyListEntry                   */
  /* -------------------------------------------------------------------------- */
  // eslint-disable-next-line max-len
  [UPDATE_PERSONAL_VOCAB_ENTRY]: async ({ commit, state }, { entryId, familiarity, headword, definition, lang = null, lemmaId }) => {
    // eslint-disable-next-line max-len
    const { response, data } = await api.updatePersonalVocabList(state.text.id, lemmaId, familiarity, headword, definition, entryId, lang);
    if (response && response.status >= 400) {
      return response;
    }
    /**
     * The code below replaces the edited personal vocab entry in the vuex state
     * to preserve the order of the vocab in the UI to streamline the user experience.
     * Note: this code does not take into account new personal vocab list data
     * if the data was updated in paralell with the editing of the personal vocab entry.
     */
    const { entries } = data;
    const { entries: localEntries } = state.vocabList;
    const foundObj = entries.find((el) => el.id === entryId);
    const localEntryIndex = localEntries.findIndex((el) => el.id === entryId);
    const updatedEntries = [...state.vocabList.entries];
    updatedEntries[localEntryIndex] = foundObj;

    commit(UPDATE_VOCAB_LIST_ENTRIES, updatedEntries);
    return null;
  },
  [CREATE_PERSONAL_VOCAB_ENTRY]: ({ commit }, { headword, definition, vocabularyListId, familiarity, lang, lemmaId }) => {
    const cb = (data) => commit(CREATE_PERSONAL_VOCAB_ENTRY, data.data);
    return api
      .createPersonalVocabEntry(headword, definition, vocabularyListId, familiarity, lang, lemmaId, cb)
      .catch(logoutOnError(commit));
  },
  [DELETE_PERSONAL_VOCAB_ENTRY]: ({ commit }, { id }) => {
    const cb = (data) => commit(DELETE_PERSONAL_VOCAB_ENTRY, data.data);
    return api.deletePersonalVocabEntry(id, cb)
      .catch(logoutOnError(commit));
  },

  /* -------------------------------------------------------------------------- */
  /*                          vocab_list.VocabularyList                         */
  /* -------------------------------------------------------------------------- */
  [FETCH_VOCAB_LIST]: async ({ commit }, { vocabListId }) => {
    const { data } = await api
      .fetchVocabList(vocabListId)
      .catch(logoutOnError(commit));
    commit(UPDATE_VOCAB_LIST, data.data);
  },
  [FETCH_VOCAB_LISTS]: async ({ commit, state }) => {
    const { data } = await api
      .fetchVocabLists(state.text.lang)
      .catch(logoutOnError(commit));
    commit(FETCH_VOCAB_LISTS, data.data);
  },
  [SET_VOCAB_LIST]: ({ commit }, { id }) => {
    commit(SET_VOCAB_LIST, id);
  },
  [TOGGLE_SHOW_IN_VOCAB_LIST]: ({ commit }) => {
    commit(TOGGLE_SHOW_IN_VOCAB_LIST);
  },
  [SET_VOCAB_LIST_TYPE]: ({ commit }, { vocabListType }) => {
    commit(SET_VOCAB_LIST_TYPE, vocabListType);
  },

  /* -------------------------------------------------------------------------- */
  /*                       vocab_list.VocabularyListEntry                       */
  /* -------------------------------------------------------------------------- */
  [CREATE_VOCAB_ENTRY]: async ({ commit }, { vocabularyListId, headword, definition, lemmaId }) => {
    const { data } = await api
      .createVocabEntry(vocabularyListId, headword, definition, lemmaId)
      .catch(logoutOnError(commit));
    commit(CREATE_VOCAB_ENTRY, data);
  },
  [UPDATE_VOCAB_ENTRY]: async ({ commit, state }, { entryId, headword, definition, lemmaId }) => {
    let data = null;
    // Hit the edit endpoint with new headword and/or definition, raise error if bad status returned
    if (headword || definition) {
      const { response, data: editData } = await api.updateVocabEntry(entryId, headword, definition);
      if (response && response.status >= 400) {
        return response;
      }
      data = editData;
    }

    // Hit the link endpoint with new lemmaId if provided, raise error if bad status returned
    if (lemmaId) {
      const { response, data: linkData } = await api.linkVocabEntry(entryId, lemmaId);
      if (response && response.status >= 400) {
        return response;
      }
      data = linkData;
    }

    // If data is still null, return a message that nothing happened.
    if (!data) {
      return {
        statusText: 'No changes were made',
        status: 204,
      };
    }

    /**
     * The code below replaces the edited personal vocab entry in the vuex state
     * to preserve the order of the vocab in the UI to streamline the user experience.
     * Note: this code does not take into account new personal vocab list data
     * if the data was updated in paralell with the editing of the personal vocab entry.
     * This code is similar to the function in UPDATE_PERSONAL_VOCAB_ENTRY, but since
     * it's hitting an endpoint that returns a single modified vocab list entry,
     * it doesn't need to look up the new entry in the results.
     */
    const { entries: localEntries } = state.vocabList;
    const localEntryIndex = localEntries.findIndex((el) => el.id === entryId);
    // Work with the entries only, rather than the whole vocab list, since
    // working with the whole list results in the table not showing the updated entry.
    const updatedEntries = [...state.vocabList.entries];
    updatedEntries[localEntryIndex] = data;

    console.log('updatedEntries:');
    console.log(updatedEntries);
    commit(UPDATE_VOCAB_LIST_ENTRIES, updatedEntries);
    return null;
  },
  [DELETE_VOCAB_ENTRY]: async ({ commit }, { id }) => {
    await api.deleteVocabEntry(id)
      .catch(logoutOnError(commit));
    commit(DELETE_VOCAB_ENTRY, id);
  },

  /* -------------------------------------------------------------------------- */
  /*                            Not accessing a model                           */
  /* -------------------------------------------------------------------------- */
  [FETCH_SUPPORTED_LANG_LIST]: ({ commit }) => (
    api.fetchSupportedLangList((data) => commit(FETCH_SUPPORTED_LANG_LIST, data.data))
      .catch(logoutOnError(commit))
  ),

  /* -------------------------------------------------------------------------- */
  /*         TODO: Delete these things, ensuring that they are not used.        */
  /* -------------------------------------------------------------------------- */
  [OLD_CREATE_VOCAB_ENTRY]: async ({ commit, state }, { lemmaId, familiarity, headword, definition }) => {
    // TODO: Make DRY with updateVocabEntry
    // TODO: this function is redundant with CREATE_PERSONAL_VOCAB_ENTRY, but works a little different.
    // Places where it is used should be adapted to use CREATE_PERSONAL_VOCAB_ENTRY and this function should be removed.
    const { response, data } = await api
      .updatePersonalVocabList(state.text.id, lemmaId, familiarity, headword, definition, null, null);
    if (response && response.status >= 400) {
      return response;
    }
    commit(FETCH_PERSONAL_VOCAB_LIST, data);
    return null;
  },
  [FETCH_NODE]: ({ commit }, { id }) => api.fetchNode(id, (data) => commit(FETCH_NODE, data)),
};
