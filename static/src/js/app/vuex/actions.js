/* eslint-disable object-curly-newline */
import {
  LEMMATIZED_TEXT_FETCH,
  LEMMATIZED_TEXT_FETCH_TOKENS,
  LEMMATIZED_TEXT_SELECT_TOKEN,
  FETCH_NODE,
  LEMMA_FETCH,
  FORMS_FETCH,
  FORMS_FETCH_PARTIAL,
  LEMMATIZED_TEXT_UPDATE_TOKEN,
  LEMMATIZED_TEXT_SET_ID,
  VOCAB_LIST_LIST,
  VOCAB_LIST_SET,
  LEMMATIZED_TEXT_SHOW_KNOWN,
  PERSONAL_VOCAB_LIST_FETCH,
  OLD_CREATE_VOCAB_ENTRY,
  VOCAB_ENTRY_UPDATE,
  PERSONAL_VOCAB_ENTRY_UPDATE,
  PROFILE_FETCH,
  PERSONAL_VOCAB_LIST_FETCH_LANG_LIST,
  PERSONAL_VOCAB_ENTRY_CREATE,
  PROFILE_SET_LANGUAGE_PREF,
  PERSONAL_VOCAB_ENTRY_DELETE,
  VOCAB_ENTRY_DELETE,
  BOOKMARK_LIST,
  BOOKMARK_CREATE,
  BOOKMARK_DELETE,
  SUPPORTED_LANG_LIST_FETCH,
  VOCAB_LIST_FETCH,
  VOCAB_LIST_SET_TYPE,
  VOCAB_ENTRY_CREATE,
  VOCAB_LIST_UPDATE,
  VOCAB_ENTRY_UPDATE_MANY,
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
  [PROFILE_FETCH]: ({ commit }) => api.profile_fetch((data) => commit(PROFILE_FETCH, data.data)),
  [PROFILE_SET_LANGUAGE_PREF]: ({ commit }, { lang }) => {
    const cb = commit(PROFILE_SET_LANGUAGE_PREF, lang);
    return api.profile_updateLang(lang, cb).catch(logoutOnError(commit));
  },

  /* -------------------------------------------------------------------------- */
  /*                             lemmatization.Form                             */
  /* -------------------------------------------------------------------------- */
  [FORMS_FETCH]: ({ commit }, { lang, form }) => api.form_fetch(lang, form, (data) => commit(FORMS_FETCH, data)),
  // Note: might be slow to looks up partial matches
  [FORMS_FETCH_PARTIAL]: ({ commit }, { lang, form }) => api.form_fetchPartial(lang, form, (data) => commit(FORMS_FETCH_PARTIAL, data)),

  /* -------------------------------------------------------------------------- */
  /*                             lemmatization.Lemma                            */
  /* -------------------------------------------------------------------------- */
  [LEMMA_FETCH]: ({ commit }, { id }) => api.lemma_fetch(id, (data) => commit(LEMMA_FETCH, data)),

  /* -------------------------------------------------------------------------- */
  /*                       lemmatized_text.LemmatizedText                       */
  /* -------------------------------------------------------------------------- */
  [LEMMATIZED_TEXT_FETCH]: ({ commit }, { id }) => api
    .lemmatizedText_fetch(id, (data) => commit(LEMMATIZED_TEXT_FETCH, data.data))
    .catch(logoutOnError(commit)),
  [LEMMATIZED_TEXT_FETCH_TOKENS]: ({ commit }, { id, vocabListId, personalVocabListId }) => {
    commit(LEMMATIZED_TEXT_SET_ID, id);
    const cb = (data) => commit(LEMMATIZED_TEXT_FETCH_TOKENS, data.data);
    return api
      .lemmatizedText_fetchTokens(id, vocabListId, personalVocabListId, cb)
      .catch(logoutOnError(commit));
  },
  [LEMMATIZED_TEXT_SELECT_TOKEN]: ({ commit, state }, { token }) => api.lemmatizedText_fetchTokenHistory(
    state.textId,
    token.tokenIndex,
    (data) => commit(LEMMATIZED_TEXT_SELECT_TOKEN, { token, data }),
  ),
  [LEMMATIZED_TEXT_UPDATE_TOKEN]: ({ commit, state }, { id, tokenIndex, lemmaId, glossIds, resolved }) => {
    // Fetch the most recent lemma data
    api
      .lemma_fetch(lemmaId, (data) => commit(LEMMA_FETCH, data))
      .catch(logoutOnError(commit));

    // Callback to commit the changes once the API call has completed
    const mutate = (data) => commit(LEMMATIZED_TEXT_UPDATE_TOKEN, data.data);

    // Perform the API request to update the token data
    return api
      .lemmatizedText_updateToken(id, tokenIndex, resolved, state.selectedVocabList, lemmaId, glossIds, null, mutate)
      .catch(logoutOnError(commit));
  },

  /* -------------------------------------------------------------------------- */
  /*                   lemmatized_text.LemmatizedTextBookmark                   */
  /* -------------------------------------------------------------------------- */
  [BOOKMARK_LIST]: ({ commit }) => (
    api
      .bookmark_list((data) => commit(BOOKMARK_LIST, data.data))
      .catch(logoutOnError(commit))
  ),
  [BOOKMARK_CREATE]: ({ dispatch, commit }, { textId }) => (
    api
      .bookmark_create(textId)
      .then(() => dispatch(BOOKMARK_LIST))
      .catch(logoutOnError(commit))
  ),
  [BOOKMARK_DELETE]: ({ dispatch, commit }, { bookmarkId }) => (
    api
      .bookmark_delete(bookmarkId)
      .then(() => dispatch(BOOKMARK_LIST))
      .catch(logoutOnError(commit))
  ),

  /* -------------------------------------------------------------------------- */
  /*                      vocab_list.PersonalVocabularyList                     */
  /* -------------------------------------------------------------------------- */
  [PERSONAL_VOCAB_LIST_FETCH]: async ({ commit }, { lang }) => {
    const { data } = await api
      .personalVocabularyList_fetch(lang)
      .catch(logoutOnError(commit));
    commit(VOCAB_LIST_UPDATE, data.data.personalVocabList);
  },
  [PERSONAL_VOCAB_LIST_FETCH_LANG_LIST]: ({ commit }) => {
    const cb = (data) => commit(PERSONAL_VOCAB_LIST_FETCH_LANG_LIST, data.data);
    return api
      .personalVocabularyList_fetchLangList(cb)
      .catch(logoutOnError(commit));
  },

  /* -------------------------------------------------------------------------- */
  /*                   vocab_list.PersonalVocabularyListEntry                   */
  /* -------------------------------------------------------------------------- */
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
  [PERSONAL_VOCAB_ENTRY_CREATE]: ({ commit }, { headword, definition, vocabularyListId, familiarity, lang, lemmaId }) => {
    const cb = (data) => commit(PERSONAL_VOCAB_ENTRY_CREATE, data.data);
    return api
      .personalVocabularyListEntry_create(headword, definition, vocabularyListId, familiarity, lang, lemmaId, cb)
      .catch(logoutOnError(commit));
  },
  [PERSONAL_VOCAB_ENTRY_DELETE]: ({ commit }, { id }) => {
    const cb = (data) => commit(PERSONAL_VOCAB_ENTRY_DELETE, data.data);
    return api.personalVocabularyListEntry_delete(id, cb)
      .catch(logoutOnError(commit));
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
  [LEMMATIZED_TEXT_SHOW_KNOWN]: ({ commit }) => {
    commit(LEMMATIZED_TEXT_SHOW_KNOWN);
  },
  [VOCAB_LIST_SET_TYPE]: ({ commit }, { vocabListType }) => {
    commit(VOCAB_LIST_SET_TYPE, vocabListType);
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

    console.log('updatedEntries:');
    console.log(updatedEntries);
    commit(VOCAB_ENTRY_UPDATE_MANY, updatedEntries);
    return null;
  },
  [VOCAB_ENTRY_DELETE]: async ({ commit }, { id }) => {
    await api.vocabularyListEntry_delete(id)
      .catch(logoutOnError(commit));
    commit(VOCAB_ENTRY_DELETE, id);
  },

  /* -------------------------------------------------------------------------- */
  /*                            Not accessing a model                           */
  /* -------------------------------------------------------------------------- */
  [SUPPORTED_LANG_LIST_FETCH]: ({ commit }) => (
    api.supportedLangList_fetch((data) => commit(SUPPORTED_LANG_LIST_FETCH, data.data))
      .catch(logoutOnError(commit))
  ),

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
