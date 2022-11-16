// hedera.Profile
export const FETCH_ME = 'fetchMe';
// TODO add language preference
export const SET_LANGUAGE_PREF = 'setLanguagePref';

// lemmatization.Form
export const FETCH_LEMMAS_BY_FORM = 'fetchLemmasByForm';
export const FETCH_LEMMAS_BY_PARTIAL_FORM = 'fetchLemmasByPartialForm';

// lemmatization.Lemma
export const FETCH_LEMMA = 'fetchLemma';
export const ADD_LEMMA = 'addLemma';

// lemmatized_text.LemmatizedText
export const FETCH_TEXT = 'fetchText';
export const SET_TEXT_ID = 'setTextId';
export const FETCH_TOKENS = 'fetchTokens';
export const UPDATE_TOKEN = 'updateToken';
export const SELECT_TOKEN = 'selectToken';

// lemmatized_text.LemmatizedTextBookmark
export const FETCH_BOOKMARKS = 'fetchBookmarks';
export const ADD_BOOKMARK = 'addBookmark';
export const REMOVE_BOOKMARK = 'removeBookmark';

// vocab_list.PersonalVocabularyList
export const FETCH_PERSONAL_VOCAB_LIST = 'fetchPersonalVocabList';
export const FETCH_PERSONAL_VOCAB_LANG_LIST = 'fetchPersonalVocabLangList';

// vocab_list.PersonalVocabularyListEntry
export const UPDATE_PERSONAL_VOCAB_ENTRY = 'updatePersonalVocabEntry';
export const CREATE_PERSONAL_VOCAB_ENTRY = 'createPersonalVocabEntry';
export const DELETE_PERSONAL_VOCAB_ENTRY = 'deletePersonalVocabEntry';

// vocab_list.VocabularyList
export const FETCH_VOCAB_LIST = 'fetchVocabList';
export const FETCH_VOCAB_LISTS = 'fetchVocabLists';
export const SET_VOCAB_LIST_TYPE = 'setVocabListType';
export const UPDATE_VOCAB_LIST = 'updateVocabList';
export const SET_VOCAB_LIST = 'setVocabList';
export const TOGGLE_SHOW_IN_VOCAB_LIST = 'toggleShowInVocabList';

// vocab_list.VocabularyListEntry
export const DELETE_VOCAB_ENTRY = 'vocabEntryDelete';
export const UPDATE_VOCAB_LIST_ENTRIES = 'updateVocabListEntries';
export const UPDATE_VOCAB_ENTRY = 'updateVocabEntry';
export const CREATE_VOCAB_ENTRY = 'createVocabEntry';

// Not accessing a model
export const FETCH_SUPPORTED_LANG_LIST = 'fetchSupportedLangList';

// Just constants, not used as function names
export const RESOLVED_NA = 'na';
export const RESOLVED_NO_LEMMA = 'no-lemma';
export const RESOLVED_UNRESOLVED = 'unresolved';
export const RESOLVED_NO_AMBIGUITY = 'no-ambiguity';
export const RESOLVED_AUTOMATIC = 'resolved-automatical';
export const RESOLVED_MANUAL = 'resolved-manual';
export const RATINGS = {
  1: 'I don\'t recognise this word',
  2: 'I recognise this word but don\'t know what it means',
  3: 'I think I know what this word means',
  4: 'I definitely know what this word means but could forget soon',
  5: 'I know this word so well, I am unlikely to ever forget it',
};

// TODO: Delete these things, ensuring that they are not used.
export const FETCH_LATTICE_NODES_BY_HEADWORD = 'fetchLatticeNodesByHeadword';
export const FETCH_NODE = 'fetchNode';
export const OLD_CREATE_VOCAB_ENTRY = 'oldCreateVocabEntry';
