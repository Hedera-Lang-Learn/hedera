import axios from 'axios';

axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.xsrfCookieName = 'csrftoken';

const BASE_URL = '/api/v1/';

export default {
  /* -------------------------------------------------------------------------- */
  /*                               hedera.Profile                               */
  /* -------------------------------------------------------------------------- */
  profile_fetch: () => axios.get(`${BASE_URL}me/`),
  profile_updateLang: (lang) => axios.post(`${BASE_URL}me/`, { lang }),

  /* -------------------------------------------------------------------------- */
  /*                             lemmatization.Form                             */
  /* -------------------------------------------------------------------------- */
  form_fetch: (lang, form, cb) => axios.get(`${BASE_URL}lemmatization/forms/${lang}/${encodeURIComponent(form)}/`).then((r) => cb(r.data)),
  form_fetchPartial: (lang, form, cb) => axios.get(`${BASE_URL}lemmatization/partial_match_forms/${lang}/${encodeURIComponent(form)}/`).then((r) => cb(r.data)),

  /* -------------------------------------------------------------------------- */
  /*                             lemmatization.Lemma                            */
  /* -------------------------------------------------------------------------- */
  lemma_fetch: (id, cb) => axios.get(`${BASE_URL}lemmatization/lemma/${id}/`).then((r) => cb(r.data)),

  /* -------------------------------------------------------------------------- */
  /*                       lemmatized_text.LemmatizedText                       */
  /* -------------------------------------------------------------------------- */
  lemmatizedText_cancel: (id, cb) => axios.post(`${BASE_URL}lemmatized_texts/${id}/cancel/`).then((r) => cb(r.data)),
  lemmatizedText_clone: (id, cb) => axios.post(`${BASE_URL}lemmatized_texts/${id}/clone/`).then((r) => cb(r.data)),
  lemmatizedText_fetch: (id, cb) => axios.get(`${BASE_URL}lemmatized_texts/${id}/detail/`).then((r) => cb(r.data)),
  lemmatizedText_fetchStatus: (id, cb) => axios.get(`${BASE_URL}lemmatized_texts/${id}/status/`).then((r) => cb(r.data)),
  lemmatizedText_fetchTokens: (id, vocabList, personalVocabList, cb) => {
    if (!vocabList && !personalVocabList) {
      return axios.get(`${BASE_URL}lemmatized_texts/${id}/`).then((r) => cb(r.data));
    }
    let qs = '';
    if (vocabList) {
      qs = `vocablist_id=${vocabList}`;
    }
    if (personalVocabList) {
      qs = `personalvocablist=${personalVocabList}`;
    }
    return axios.get(`${BASE_URL}lemmatized_texts/${id}/?${qs}`).then((r) => cb(r.data));
  },
  lemmatizedText_fetchTokenHistory: (id, tokenIndex, cb) => axios.get(`${BASE_URL}lemmatized_texts/${id}/tokens/${tokenIndex}/history/`).then((r) => cb(r.data)),
  lemmatizedText_list: (cb) => axios.get(`${BASE_URL}lemmatized_texts/`).then((r) => cb(r.data)),
  lemmatizedText_retry: (id, cb) => axios.post(`${BASE_URL}lemmatized_texts/${id}/retry/`).then((r) => cb(r.data)),
  lemmatizedText_updateToken: (id, tokenIndex, resolved, vocabList, lemmaId = null, glossIds = [], lemma = null, cb) => {
    if (vocabList === null) {
      return axios.post(`${BASE_URL}lemmatized_texts/${id}/`, {
        tokenIndex,
        lemmaId,
        glossIds,
        lemma,
        resolved,
      }).then((r) => cb(r.data));
    }
    return axios.post(`${BASE_URL}lemmatized_texts/${id}/?vocablist_id=${vocabList}`, {
      tokenIndex,
      lemmaId,
      glossIds,
      lemma,
      resolved,
    }).then((r) => cb(r.data));
  },

  /* -------------------------------------------------------------------------- */
  /*                   lemmatized_text.LemmatizedTextBookmark                   */
  /* -------------------------------------------------------------------------- */
  bookmark_create: (textId) => axios.post(`${BASE_URL}bookmarks/`, { textId }),
  bookmark_delete: (bookmarkId) => axios.delete(`${BASE_URL}bookmarks/${bookmarkId}/`),
  bookmark_list: (cb) => axios.get(`${BASE_URL}bookmarks/`).then((r) => cb(r.data)),

  /* -------------------------------------------------------------------------- */
  /*                      vocab_list.PersonalVocabularyList                     */
  /* -------------------------------------------------------------------------- */
  personalVocabularyList_fetch: (lang) => axios.get(`${BASE_URL}personal_vocab_list/?lang=${lang}`),
  personalVocabularyList_fetchLangList: () => axios.get(`${BASE_URL}personal_vocab_list/quick_add/`),
  personalVocabularyList_update: (textId, lemmaId, familiarity, headword, definition, entryId, lang) => {
    let data = {
      familiarity, headword, definition, lemmaId,
    };
    if (lang !== null && entryId !== null) {
      return axios.post(`${BASE_URL}personal_vocab_list/${entryId}/?lang=${lang}`, data).then((r) => r.data).catch((error) => error);
    }
    if (entryId !== null) {
      return axios.post(`${BASE_URL}personal_vocab_list/${entryId}/?text=${textId}`, data).then((r) => r.data).catch((error) => error);
    }
    data = { ...data, lemmaId };
    return axios.post(`${BASE_URL}personal_vocab_list/?text=${textId}`, data).then((r) => r.data).catch((error) => error);
  },

  /* -------------------------------------------------------------------------- */
  /*                   vocab_list.PersonalVocabularyListEntry                   */
  /* -------------------------------------------------------------------------- */
  personalVocabularyListEntry_create: (headword, definition, vocabularyListId, familiarity, lang, lemmaId) => {
    const payload = {
      headword,
      definition,
      familiarity,
      vocabulary_list_id: vocabularyListId,
      lang,
      lemma_id: lemmaId,
    };
    return axios.post(`${BASE_URL}personal_vocab_list/quick_add/`, payload);
  },
  personalVocabularyListEntry_delete: (id) => axios.delete(`${BASE_URL}personal_vocab_list/`, { data: { id } }),

  /* -------------------------------------------------------------------------- */
  /*                          vocab_list.VocabularyList                         */
  /* -------------------------------------------------------------------------- */
  vocabularyList_fetch: (vocabListId) => axios.get(`${BASE_URL}vocab_lists/${vocabListId}`),
  vocabularyList_list: (lang) => axios.get(`${BASE_URL}vocab_lists/?lang=${lang}`),

  /* -------------------------------------------------------------------------- */
  /*                       vocab_list.VocabularyListEntry                       */
  /* -------------------------------------------------------------------------- */
  vocabularyListEntry_create: (vocabularyListId, headword, definition, lemmaId) => {
    const payload = {
      headword,
      definition,
    };
    if (lemmaId) {
      payload.lemma_id = lemmaId;
    }
    return axios.post(`${BASE_URL}vocab_lists/${vocabularyListId}/entries/`, payload);
  },
  vocabularyListEntry_delete: (id) => axios.post(`${BASE_URL}vocab_entries/${id}/delete/`),
  vocabularyListEntry_link: (id, lemmaId) => axios.post(`${BASE_URL}vocab_entries/${id}/link/`, { lemma_id: lemmaId }),
  vocabularyListEntry_list: (id, cb) => axios.get(`${BASE_URL}vocab_lists/${id}/entries/`).then((r) => cb(r.data)),
  vocabularyListEntry_update: (id, headword, definition) => axios.post(`${BASE_URL}vocab_entries/${id}/edit/`, { headword, definition }),

  /* -------------------------------------------------------------------------- */
  /*                            Not accessing a model                           */
  /* -------------------------------------------------------------------------- */
  supportedLangList_fetch: (cb) => axios.get(`${BASE_URL}supported_languages/`).then((r) => cb(r.data)),

  /* -------------------------------------------------------------------------- */
  /*         TODO: Delete these things, ensuring that they are not used.        */
  /* -------------------------------------------------------------------------- */
  fetchNode: (id, cb) => axios.get(`/lattices/${id}.json`).then((r) => cb(r.data)),
  fetchLatticeNodes: (headword, lang, cb) => axios.get(`${BASE_URL}lattice_nodes/?headword=${headword}&lang=${lang}`).then((r) => cb(r.data)),
};
