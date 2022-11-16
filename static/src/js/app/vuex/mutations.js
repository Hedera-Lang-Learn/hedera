import {
  FETCH_TOKENS,
  SELECT_TOKEN,
  FETCH_NODE,
  FETCH_LEMMA,
  FETCH_LEMMAS_BY_FORM,
  UPDATE_TOKEN,
  SET_TEXT_ID,
  FETCH_VOCAB_LISTS,
  SET_VOCAB_LIST,
  TOGGLE_SHOW_IN_VOCAB_LIST,
  FETCH_TEXT,
  FETCH_PERSONAL_VOCAB_LIST,
  FETCH_ME,
  FETCH_PERSONAL_VOCAB_LANG_LIST,
  CREATE_PERSONAL_VOCAB_ENTRY,
  FETCH_LATTICE_NODES_BY_HEADWORD,
  SET_LANGUAGE_PREF,
  DELETE_PERSONAL_VOCAB_ENTRY,
  FETCH_BOOKMARKS,
  FETCH_SUPPORTED_LANG_LIST,
  FETCH_LEMMAS_BY_PARTIAL_FORM,
  FETCH_VOCAB_LIST,
  DELETE_VOCAB_ENTRY,
  SET_VOCAB_LIST_TYPE,
  CREATE_VOCAB_ENTRY,
  UPDATE_VOCAB_LIST,
  UPDATE_VOCAB_LIST_ENTRIES,
} from '../constants';

export default {
  /* -------------------------------------------------------------------------- */
  /*                               hedera.Profile                               */
  /* -------------------------------------------------------------------------- */
  [FETCH_ME]: (state, data) => {
    state.me = data;
  },
  [SET_LANGUAGE_PREF]: (state, data) => {
    state.me = data;
  },

  /* -------------------------------------------------------------------------- */
  /*                             lemmatization.Form                             */
  /* -------------------------------------------------------------------------- */
  [FETCH_LEMMAS_BY_FORM]: (state, data) => {
    const form = data.data;
    state.forms = {
      ...state.forms,
      [form.form]: form,
    };
  },
  [FETCH_LEMMAS_BY_PARTIAL_FORM]: (state, data) => {
    const forms = data.data;
    state.partialMatchForms = [...forms];
  },

  /* -------------------------------------------------------------------------- */
  /*                             lemmatization.Lemma                            */
  /* -------------------------------------------------------------------------- */
  [FETCH_LEMMA]: (state, data) => {
    const lemma = data.data;
    state.lemmas = {
      ...state.lemmas,
      [lemma.pk]: lemma,
    };
  },

  /* -------------------------------------------------------------------------- */
  /*                       lemmatized_text.LemmatizedText                       */
  /* -------------------------------------------------------------------------- */
  [FETCH_TEXT]: (state, data) => {
    state.text = data;
  },
  [SET_TEXT_ID]: (state, id) => {
    state.textId = id;
  },
  [FETCH_TOKENS]: (state, data) => {
    state.tokens = data;
  },
  [SELECT_TOKEN]: (state, { token, data }) => {
    state.selectedToken = token;
    state.selectedTokenHistory = data.data.tokenHistory;
  },
  [UPDATE_TOKEN]: (state, data) => {
    state.tokens = data.tokens;
    state.selectedTokenHistory = data.tokenHistory;
    if (state.selectedToken) {
      state.selectedToken = state.tokens[state.selectedToken.tokenIndex];
    }
  },

  /* -------------------------------------------------------------------------- */
  /*                   lemmatized_text.LemmatizedTextBookmark                   */
  /* -------------------------------------------------------------------------- */
  [FETCH_BOOKMARKS]: (state, data) => {
    state.bookmarks = data;
  },

  /* -------------------------------------------------------------------------- */
  /*                      vocab_list.PersonalVocabularyList                     */
  /* -------------------------------------------------------------------------- */
  [FETCH_PERSONAL_VOCAB_LANG_LIST]: (state, data) => {
    state.personalVocabLangList = data;
  },

  /* -------------------------------------------------------------------------- */
  /*                   vocab_list.PersonalVocabularyListEntry                   */
  /* -------------------------------------------------------------------------- */
  [FETCH_PERSONAL_VOCAB_LIST]: (state, data) => {
    state.vocabList = data;
  },
  [CREATE_PERSONAL_VOCAB_ENTRY]: (state, data) => {
    state.vocabAdded = data.created;
    if (state.vocabList.entries) {
      state.vocabList.entries = [data.data, ...state.vocabList.entries];
    }
  },
  [DELETE_PERSONAL_VOCAB_ENTRY]: (state, data) => {
    const index = state.vocabList.entries.findIndex((vocab) => vocab.id === data.id);
    if (index >= 0) state.vocabList.entries.splice(index, 1);
  },

  /* -------------------------------------------------------------------------- */
  /*                          vocab_list.VocabularyList                         */
  /* -------------------------------------------------------------------------- */
  [UPDATE_VOCAB_LIST]: (state, data) => {
    state.vocabList = data;
  },
  [FETCH_VOCAB_LIST]: (state, data) => {
    state.vocabList = data;
  },
  [FETCH_VOCAB_LISTS]: (state, data) => {
    state.vocabLists = data;
  },
  [SET_VOCAB_LIST]: (state, id) => {
    state.selectedVocabList = id;
  },
  [TOGGLE_SHOW_IN_VOCAB_LIST]: (state) => {
    state.showInVocabList = !state.showInVocabList;
  },
  [SET_VOCAB_LIST_TYPE]: (state, vocabListType) => {
    state.vocabListType = vocabListType;
  },

  /* -------------------------------------------------------------------------- */
  /*                       vocab_list.VocabularyListEntry                       */
  /* -------------------------------------------------------------------------- */
  [UPDATE_VOCAB_LIST_ENTRIES]: (state, updatedEntries) => {
    state.vocabList.entries = updatedEntries;
  },
  [CREATE_VOCAB_ENTRY]: (state, data) => {
    state.vocabAdded = data.id;
    if (state.vocabList.entries) {
      state.vocabList.entries = [data, ...state.vocabList.entries];
    }
  },
  [DELETE_VOCAB_ENTRY]: (state, id) => {
    const index = state.vocabList.entries.findIndex((vocab) => vocab.id === id);
    if (index >= 0) state.vocabList.entries.splice(index, 1);
  },

  /* -------------------------------------------------------------------------- */
  /*                            Not accessing a model                           */
  /* -------------------------------------------------------------------------- */
  [FETCH_SUPPORTED_LANG_LIST]: (state, data) => {
    state.supportedLanguages = data;
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
