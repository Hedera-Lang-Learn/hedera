import {
  BOOKMARK_LIST,
  FETCH_LATTICE_NODES_BY_HEADWORD,
  FETCH_NODE,
  FORMS_FETCH_PARTIAL,
  FORMS_FETCH,
  LEMMA_FETCH,
  LEMMAS_FETCH_PARTIAL,
  LEMMATIZED_TEXT_FETCH_TOKENS,
  LEMMATIZED_TEXT_FETCH_LIST,
  LEMMATIZED_TEXT_FETCH,
  LEMMATIZED_TEXT_SELECT_TOKEN,
  LEMMATIZED_TEXT_SET_ID,
  LEMMATIZED_TEXT_SHOW_KNOWN,
  LEMMATIZED_TEXT_UPDATE_TOKEN,
  PERSONAL_VOCAB_ENTRY_CREATE,
  PERSONAL_VOCAB_ENTRY_DELETE,
  PERSONAL_VOCAB_LIST_FETCH_LANG_LIST,
  PERSONAL_VOCAB_LIST_FETCH,
  PERSONAL_VOCAB_ENTRY_UPDATE_MANY,
  PROFILE_FETCH,
  PROFILE_SET_LANGUAGE_PREF,
  SUPPORTED_LANG_LIST_FETCH,
  VOCAB_ENTRY_CREATE,
  VOCAB_ENTRY_DELETE,
  VOCAB_ENTRY_UPDATE_MANY,
  VOCAB_LIST_FETCH,
  VOCAB_LIST_LIST,
  VOCAB_LIST_SET_TYPE,
  VOCAB_LIST_SET,
  VOCAB_LIST_UPDATE,
} from '../constants';

export default {
  /* -------------------------------------------------------------------------- */
  /*                               hedera.Profile                               */
  /* -------------------------------------------------------------------------- */
  [PROFILE_FETCH]: (state, data) => {
    state.me = data;
  },
  [PROFILE_SET_LANGUAGE_PREF]: (state, data) => {
    state.me = data;
  },

  /* -------------------------------------------------------------------------- */
  /*                             lemmatization.Form                             */
  /* -------------------------------------------------------------------------- */
  [FORMS_FETCH]: (state, data) => {
    const { form } = data;
    state.forms = {
      ...state.forms,
      [form]: data,
    };
  },
  [FORMS_FETCH_PARTIAL]: (state, data) => {
    const forms = data.data;
    state.partialMatchForms = [...forms];
  },

  /* -------------------------------------------------------------------------- */
  /*                             lemmatization.Lemma                            */
  /* -------------------------------------------------------------------------- */
  [LEMMA_FETCH]: (state, data) => {
    const lemma = data;
    state.lemmas = {
      ...state.lemmas,
      [lemma.pk]: lemma,
    };
  },
  [LEMMAS_FETCH_PARTIAL]: (state, data) => {
    const lemmas = data.data;
    state.partialMatchLemmas = [...lemmas];
  },

  /* -------------------------------------------------------------------------- */
  /*                       lemmatized_text.LemmatizedText                       */
  /* -------------------------------------------------------------------------- */
  [LEMMATIZED_TEXT_FETCH_LIST]: (state, data) => {
    state.texts = data.data.map((lemmatizedText) => ({
      ...lemmatizedText.text,
      stats: lemmatizedText.stats,
    }));
  },
  [LEMMATIZED_TEXT_FETCH]: (state, data) => {
    state.text = data.data;
  },
  [LEMMATIZED_TEXT_FETCH_TOKENS]: (state, data) => {
    state.tokens = data.data;
  },
  [LEMMATIZED_TEXT_SELECT_TOKEN]: (state, { token, data }) => {
    state.selectedToken = token;
    state.selectedTokenHistory = data.data.tokenHistory;
  },
  [LEMMATIZED_TEXT_SET_ID]: (state, id) => {
    state.textId = id;
  },
  [LEMMATIZED_TEXT_SHOW_KNOWN]: (state) => {
    state.showInVocabList = !state.showInVocabList;
  },
  [LEMMATIZED_TEXT_UPDATE_TOKEN]: (state, data) => {
    state.tokens = data.tokens;
    state.selectedTokenHistory = data.tokenHistory;
    if (state.selectedToken) {
      state.selectedToken = state.tokens[state.selectedToken.tokenIndex];
    }
  },

  /* -------------------------------------------------------------------------- */
  /*                   lemmatized_text.LemmatizedTextBookmark                   */
  /* -------------------------------------------------------------------------- */
  [BOOKMARK_LIST]: (state, data) => {
    state.bookmarks = data.data;
  },

  /* -------------------------------------------------------------------------- */
  /*                      vocab_list.PersonalVocabularyList                     */
  /* -------------------------------------------------------------------------- */
  [PERSONAL_VOCAB_LIST_FETCH]: (state, data) => {
    state.personalVocabList = data;
  },
  [PERSONAL_VOCAB_LIST_FETCH_LANG_LIST]: (state, data) => {
    state.personalVocabLangList = data;
  },

  /* -------------------------------------------------------------------------- */
  /*                   vocab_list.PersonalVocabularyListEntry                   */
  /* -------------------------------------------------------------------------- */
  [PERSONAL_VOCAB_ENTRY_CREATE]: (state, data) => {
    state.vocabAdded = data.created;
    if (state.personalVocabList.entries) {
      state.personalVocabList.entries = [data.data, ...state.personalVocabList.entries];
    }
  },
  [PERSONAL_VOCAB_ENTRY_DELETE]: (state, data) => {
    const index = state.personalVocabList.entries.findIndex((vocab) => vocab.id === data.id);
    if (index >= 0) state.personalVocabList.entries.splice(index, 1);
  },
  [PERSONAL_VOCAB_ENTRY_UPDATE_MANY]: (state, updatedEntries) => {
    state.personalVocabList.entries = updatedEntries;
  },

  /* -------------------------------------------------------------------------- */
  /*                          vocab_list.VocabularyList                         */
  /* -------------------------------------------------------------------------- */
  [VOCAB_LIST_FETCH]: (state, data) => {
    state.vocabList = data;
  },
  [VOCAB_LIST_LIST]: (state, data) => {
    state.vocabLists = data;
  },
  [VOCAB_LIST_SET]: (state, id) => {
    if (state.selectedVocabList.indexOf(id) === -1) {
      state.selectedVocabList.push(id);
    } else {
      const index = state.selectedVocabList.indexOf(id);
      state.selectedVocabList.splice(index, 1);
    }
  },
  [VOCAB_LIST_SET_TYPE]: (state, vocabListType) => {
    state.vocabListType = vocabListType;
  },
  [VOCAB_LIST_UPDATE]: (state, data) => {
    state.vocabList = data;
  },

  /* -------------------------------------------------------------------------- */
  /*                       vocab_list.VocabularyListEntry                       */
  /* -------------------------------------------------------------------------- */
  [VOCAB_ENTRY_CREATE]: (state, data) => {
    state.vocabAdded = data.id;
    if (state.vocabList.entries) {
      state.vocabList.entries = [data, ...state.vocabList.entries];
    }
  },
  [VOCAB_ENTRY_DELETE]: (state, id) => {
    const index = state.vocabList.entries.findIndex((vocab) => vocab.id === id);
    if (index >= 0) state.vocabList.entries.splice(index, 1);
  },
  [VOCAB_ENTRY_UPDATE_MANY]: (state, updatedEntries) => {
    state.vocabList.entries = updatedEntries;
  },

  /* -------------------------------------------------------------------------- */
  /*                            Not accessing a model                           */
  /* -------------------------------------------------------------------------- */
  [SUPPORTED_LANG_LIST_FETCH]: (state, data) => {
    state.supportedLanguages = data.data;
  },

  /* -------------------------------------------------------------------------- */
  /*         TODO: Delete these things, ensuring that they are not used.        */
  /* -------------------------------------------------------------------------- */
  [FETCH_NODE]: (state, data) => {
    state.nodes = {
      ...state.nodes,
      [data.pk]: data,
    };
  },
  [FETCH_LATTICE_NODES_BY_HEADWORD]: (state, data) => {
    state.latticeNodes = data;
  },
};
