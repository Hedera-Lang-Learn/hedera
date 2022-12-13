/* eslint-disable object-curly-newline */
import {
  BOOKMARK_CREATE,
  BOOKMARK_DELETE,
  BOOKMARK_LIST,
  FETCH_NODE,
  FORMS_FETCH_PARTIAL,
  FORMS_FETCH,
  LEMMA_FETCH,
  LEMMATIZED_TEXT_FETCH_TOKENS,
  LEMMATIZED_TEXT_FETCH,
  LEMMATIZED_TEXT_SELECT_TOKEN,
  LEMMATIZED_TEXT_SET_ID,
  LEMMATIZED_TEXT_SHOW_KNOWN,
  LEMMATIZED_TEXT_UPDATE_TOKEN,
  OLD_CREATE_VOCAB_ENTRY,
  PERSONAL_VOCAB_ENTRY_CREATE,
  PERSONAL_VOCAB_ENTRY_DELETE,
  PERSONAL_VOCAB_ENTRY_UPDATE,
  PERSONAL_VOCAB_LIST_FETCH_LANG_LIST,
  PERSONAL_VOCAB_LIST_FETCH,
  PROFILE_FETCH,
  PROFILE_SET_LANGUAGE_PREF,
  SUPPORTED_LANG_LIST_FETCH,
  VOCAB_ENTRY_CREATE,
  VOCAB_ENTRY_DELETE,
  VOCAB_ENTRY_UPDATE_MANY,
  VOCAB_ENTRY_UPDATE,
  VOCAB_LIST_FETCH,
  VOCAB_LIST_LIST,
  VOCAB_LIST_SET_TYPE,
  VOCAB_LIST_SET,
  VOCAB_LIST_UPDATE,
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
  [PROFILE_FETCH]: async ({ commit }) => {
    // get `data` property of axios response, where response data is
    const { data } = await api.profile_fetch();
    // in the commit, still need to get data.data because that's how the api response wraps it
    commit(PROFILE_FETCH, data.data);
  },
  [PROFILE_SET_LANGUAGE_PREF]: async ({ commit }, { lang }) => {
    const { data } = await api.profile_updateLang(lang);
    commit(PROFILE_SET_LANGUAGE_PREF, data.data.lang);
  },

  /* -------------------------------------------------------------------------- */
  /*                             lemmatization.Form                             */
  /* -------------------------------------------------------------------------- */
  [FORMS_FETCH]: async ({ commit }, { lang, form }) => {
    const response = await api.form_fetch(lang, form);
    commit(FORMS_FETCH, response);
  },
  // Note: might be slow to looks up partial matches
  [FORMS_FETCH_PARTIAL]: async ({ commit }, { lang, form }) => {
    const response = await api.form_fetchPartial(lang, form);
    commit(FORMS_FETCH_PARTIAL, response);
  },

  /* -------------------------------------------------------------------------- */
  /*                             lemmatization.Lemma                            */
  /* -------------------------------------------------------------------------- */
  [LEMMA_FETCH]: async ({ commit }, { id }) => {
    const response = await api.lemma_fetch(id);
    commit(LEMMA_FETCH, response);
  },

  /* -------------------------------------------------------------------------- */
  /*                       lemmatized_text.LemmatizedText                       */
  /* -------------------------------------------------------------------------- */
  [LEMMATIZED_TEXT_FETCH]: async ({ commit }, { id }) => {
    const { data } = await api.lemmatizedText_fetch(id);
    commit(LEMMATIZED_TEXT_FETCH, data);
  },
  [LEMMATIZED_TEXT_FETCH_TOKENS]: async ({ commit }, { id, vocabListId, personalVocabListId }) => {
    commit(LEMMATIZED_TEXT_SET_ID, id);
    const { data } = await api.lemmatizedText_fetchTokens(id, vocabListId, personalVocabListId);
    commit(LEMMATIZED_TEXT_FETCH_TOKENS, data);
  },
  [LEMMATIZED_TEXT_SELECT_TOKEN]: async ({ commit, state }, { token }) => {
    const response = await api.lemmatizedText_fetchTokenHistory(
      state.textId,
      token.tokenIndex,
    );
    commit(LEMMATIZED_TEXT_SELECT_TOKEN, { token, data: response });
  },
  [LEMMATIZED_TEXT_UPDATE_TOKEN]: async (
    { commit, state },
    { id, tokenIndex, lemmaId, glossIds, resolved },
  ) => {
    // Fetch the most recent lemma data
    const response = await api.lemma_fetch(lemmaId);
    commit(LEMMA_FETCH, response);
    // Perform the API request to update the token data
    const { data } = await api.lemmatizedText_updateToken(
      id,
      tokenIndex,
      resolved,
      state.selectedVocabList,
      lemmaId,
      glossIds,
      null,
    );
    commit(LEMMATIZED_TEXT_UPDATE_TOKEN, data);
  },

  /* -------------------------------------------------------------------------- */
  /*                   lemmatized_text.LemmatizedTextBookmark                   */
  /* -------------------------------------------------------------------------- */
  [BOOKMARK_CREATE]: async ({ dispatch }, { textId }) => {
    await api.bookmark_create(textId);
    dispatch(BOOKMARK_LIST);
  },
  [BOOKMARK_DELETE]: async ({ dispatch }, { bookmarkId }) => {
    await api.bookmark_delete(bookmarkId);
    dispatch(BOOKMARK_LIST);
  },
  [BOOKMARK_LIST]: async ({ commit }) => {
    const { data } = await api.bookmark_list();
    commit(BOOKMARK_LIST, data);
  },

  /* -------------------------------------------------------------------------- */
  /*                      vocab_list.PersonalVocabularyList                     */
  /* -------------------------------------------------------------------------- */
  [PERSONAL_VOCAB_LIST_FETCH]: async ({ commit }, { lang }) => {
    const { data } = await api
      .personalVocabularyList_fetch(lang)
      .catch(logoutOnError(commit));
    commit(VOCAB_LIST_UPDATE, data.data.personalVocabList);
  },
  [PERSONAL_VOCAB_LIST_FETCH_LANG_LIST]: async ({ commit }) => {
    const { data } = await api.personalVocabularyList_fetchLangList();
    commit(PERSONAL_VOCAB_LIST_FETCH_LANG_LIST, data.data);
  },

  /* -------------------------------------------------------------------------- */
  /*                   vocab_list.PersonalVocabularyListEntry                   */
  /* -------------------------------------------------------------------------- */
  [PERSONAL_VOCAB_ENTRY_CREATE]: async ({ commit }, { headword, definition, vocabularyListId, familiarity, lang, lemmaId }) => {
    const { data } = await api.personalVocabularyListEntry_create(
      headword,
      definition,
      vocabularyListId,
      familiarity,
      lang,
      lemmaId,
    );
    commit(PERSONAL_VOCAB_ENTRY_CREATE, data.data);
  },
  [PERSONAL_VOCAB_ENTRY_DELETE]: async ({ commit }, { id }) => {
    const { data } = await api.personalVocabularyListEntry_delete(id);
    commit(PERSONAL_VOCAB_ENTRY_DELETE, data);
  },
  // eslint-disable-next-line max-len
  [PERSONAL_VOCAB_ENTRY_UPDATE]: async ({ commit, state }, { entryId, familiarity, headword, definition, lang = null, lemmaId }) => {
    // eslint-disable-next-line max-len
    const { response, data } = await api.personalVocabularyList_update(state.text.id, lemmaId, familiarity, headword, definition, entryId, lang);
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

    commit(VOCAB_ENTRY_UPDATE_MANY, updatedEntries);
    return null;
  },

  /* -------------------------------------------------------------------------- */
  /*                          vocab_list.VocabularyList                         */
  /* -------------------------------------------------------------------------- */
  [VOCAB_LIST_FETCH]: async ({ commit }, { vocabListId }) => {
    const { data } = await api
      .vocabularyList_fetch(vocabListId)
      .catch(logoutOnError(commit));
    commit(VOCAB_LIST_UPDATE, data.data);
  },
  [VOCAB_LIST_LIST]: async ({ commit, state }) => {
    const { data } = await api
      .vocabularyList_list(state.text.lang)
      .catch(logoutOnError(commit));
    commit(VOCAB_LIST_LIST, data.data);
  },
  [VOCAB_LIST_SET]: ({ commit }, { id }) => {
    commit(VOCAB_LIST_SET, id);
  },
  [VOCAB_LIST_SET_TYPE]: ({ commit }, { vocabListType }) => {
    commit(VOCAB_LIST_SET_TYPE, vocabListType);
  },
  [LEMMATIZED_TEXT_SHOW_KNOWN]: ({ commit }) => {
    commit(LEMMATIZED_TEXT_SHOW_KNOWN);
  },

  /* -------------------------------------------------------------------------- */
  /*                       vocab_list.VocabularyListEntry                       */
  /* -------------------------------------------------------------------------- */
  [VOCAB_ENTRY_CREATE]: async ({ commit }, { vocabularyListId, headword, definition, lemmaId }) => {
    const { data } = await api
      .vocabularyListEntry_create(vocabularyListId, headword, definition, lemmaId)
      .catch(logoutOnError(commit));
    commit(VOCAB_ENTRY_CREATE, data);
  },
  [VOCAB_ENTRY_DELETE]: async ({ commit }, { id }) => {
    await api.vocabularyListEntry_delete(id)
      .catch(logoutOnError(commit));
    commit(VOCAB_ENTRY_DELETE, id);
  },
  [VOCAB_ENTRY_UPDATE]: async ({ commit, state }, { entryId, headword, definition, lemmaId }) => {
    let data = null;
    // Hit the edit endpoint with new headword and/or definition, raise error if bad status returned
    if (headword || definition) {
      const { response, data: editData } = await api.vocabularyListEntry_update(entryId, headword, definition);
      if (response && response.status >= 400) {
        return response;
      }
      data = editData;
    }

    // Hit the link endpoint with new lemmaId if provided, raise error if bad status returned
    if (lemmaId) {
      const { response, data: linkData } = await api.vocabularyListEntry_link(entryId, lemmaId);
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
     * This code is similar to the function in PERSONAL_VOCAB_ENTRY_UPDATE, but since
     * it's hitting an endpoint that returns a single modified vocab list entry,
     * it doesn't need to look up the new entry in the results.
     */
    const { entries: localEntries } = state.vocabList;
    const localEntryIndex = localEntries.findIndex((el) => el.id === entryId);
    // Work with the entries only, rather than the whole vocab list, since
    // working with the whole list results in the table not showing the updated entry.
    const updatedEntries = [...state.vocabList.entries];
    updatedEntries[localEntryIndex] = data;

    commit(VOCAB_ENTRY_UPDATE_MANY, updatedEntries);
    return null;
  },

  /* -------------------------------------------------------------------------- */
  /*                            Not accessing a model                           */
  /* -------------------------------------------------------------------------- */
  [SUPPORTED_LANG_LIST_FETCH]: async ({ commit }) => {
    const { data } = await api.supportedLangList_fetch();
    commit(SUPPORTED_LANG_LIST_FETCH, data);
  },

  /* -------------------------------------------------------------------------- */
  /*         TODO: Delete these things, ensuring that they are not used.        */
  /* -------------------------------------------------------------------------- */
  [OLD_CREATE_VOCAB_ENTRY]: async ({ commit, state }, { lemmaId, familiarity, headword, definition }) => {
    // TODO: Make DRY with updateVocabEntry
    // TODO: this function is redundant with PERSONAL_VOCAB_ENTRY_CREATE, but works a little different.
    // Places where it is used should be adapted to use PERSONAL_VOCAB_ENTRY_CREATE and this function should be removed.
    const { response, data } = await api
      .personalVocabularyList_update(state.text.id, lemmaId, familiarity, headword, definition, null, null);
    if (response && response.status >= 400) {
      return response;
    }
    commit(PERSONAL_VOCAB_LIST_FETCH, data);
    return null;
  },
  [FETCH_NODE]: ({ commit }, { id }) => api.fetchNode(id, (data) => commit(FETCH_NODE, data)),
};
