// hedera.Profile
export const PROFILE_FETCH = 'profile_fetch';
// TODO add language preference
export const PROFILE_SET_LANGUAGE_PREF = 'profile_setLanguagePref';

// lemmatization.Form
export const FORMS_FETCH = 'forms_fetch';
export const FORMS_FETCH_PARTIAL = 'forms_fetchPartial';

// lemmatization.Lemma
export const LEMMA_CREATE = 'lemma_create';
export const LEMMA_FETCH = 'lemma_fetch';
export const LEMMAS_FETCH_PARTIAL = 'lemmas_fetchPartial';

// lemmatized_text.LemmatizedText
export const LEMMATIZED_TEXT_FETCH = 'lemmatizedText_fetch';
export const LEMMATIZED_TEXT_FETCH_LIST = 'lemmatizedText_fetchList';
export const LEMMATIZED_TEXT_FETCH_TOKENS = 'lemmatizedText_fetchTokens';
export const LEMMATIZED_TEXT_SELECT_TOKEN = 'lemmatizedText_selectToken';
export const LEMMATIZED_TEXT_SET_ID = 'lemmatizedText_setId';
export const LEMMATIZED_TEXT_SHOW_KNOWN = 'lemmatizedText_showKnown';
export const LEMMATIZED_TEXT_UPDATE_TOKEN = 'lemmatizedText_updateToken';

// lemmatized_text.LemmatizedTextBookmark
export const BOOKMARK_CREATE = 'bookmark_create';
export const BOOKMARK_DELETE = 'bookmark_delete';
export const BOOKMARK_LIST = 'bookmark_list';
export const BOOKMARK_FETCH = 'bookmark_fetch';

// vocab_list.PersonalVocabularyList
export const PERSONAL_VOCAB_LIST_FETCH = 'personalVocabularyList_fetch';
export const PERSONAL_VOCAB_LIST_FETCH_LANG_LIST =
  'personalVocabularyList_fetchLangList';

// vocab_list.PersonalVocabularyListEntry
export const PERSONAL_VOCAB_ENTRY_CREATE = 'personalVocabularyListEntry_create';
export const PERSONAL_VOCAB_ENTRY_DELETE = 'personalVocabularyListEntry_delete';
export const PERSONAL_VOCAB_ENTRY_UPDATE = 'personalVocabularyListEntry_update';
export const PERSONAL_VOCAB_ENTRY_UPDATE_MANY =
  'personalVocabularyListEntry_updateMany';

// vocab_list.VocabularyList
export const VOCAB_LIST_FETCH = 'vocabularyList_fetch';
export const VOCAB_LIST_LIST = 'vocabularyList_list';
export const VOCAB_LIST_SET = 'vocabularyList_set';
export const VOCAB_LIST_SET_TYPE = 'vocabularyList_setType';
export const VOCAB_LIST_UPDATE = 'vocabularyList_update';

// vocab_list.VocabularyListEntry
export const VOCAB_ENTRY_CREATE = 'vocabularyListEntry_create';
export const VOCAB_ENTRY_DELETE = 'vocabularyListEntry_delete';
export const VOCAB_ENTRY_UPDATE = 'vocabularyListEntry_update';
export const VOCAB_ENTRY_UPDATE_MANY = 'vocabularyListEntry_updateMany';

// Not accessing a model
export const SUPPORTED_LANG_LIST_FETCH = 'supportedLangList_fetch';

// Just constants, not used as function names
export const RESOLVED_NA = 'na';
export const RESOLVED_NO_LEMMA = 'no-lemma';
export const RESOLVED_UNRESOLVED = 'unresolved';
export const RESOLVED_NO_AMBIGUITY = 'no-ambiguity';
export const RESOLVED_AUTOMATIC = 'resolved-automatical';
export const RESOLVED_MANUAL = 'resolved-manual';
export const RATINGS = {
  1: "I don't recognise this word",
  2: "I recognise this word but don't know what it means",
  3: 'I think I know what this word means',
  4: 'I definitely know what this word means but could forget soon',
  5: 'I know this word so well, I am unlikely to ever forget it',
};

// TODO: Delete these things, ensuring that they are not used.
export const FETCH_LATTICE_NODES_BY_HEADWORD = 'fetchLatticeNodesByHeadword';
export const FETCH_NODE = 'fetchNode';
export const OLD_CREATE_VOCAB_ENTRY = 'oldCreateVocabEntry';
