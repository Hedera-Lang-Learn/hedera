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
  form_fetch: (lang, form) => axios.get(
    `${BASE_URL}lemmatization/forms/${lang}/${encodeURIComponent(form)}/`,
  ),
  form_fetchPartial: (lang, form) => axios
    .get(
      `${BASE_URL}lemmatization/partial_match_forms/${lang}/${encodeURIComponent(
        form,
      )}/`,
    )
    .then((r) => r.data),

  /* -------------------------------------------------------------------------- */
  /*                             lemmatization.Lemma                            */
  /* -------------------------------------------------------------------------- */
  lemma_fetch: (id) => axios.get(`${BASE_URL}lemmatization/lemma/${id}/`),
  lemmas_fetchPartial: (lang, lemma) => axios
    .get(
      `${BASE_URL}lemmatization/partial_match_lemmas/${lang}/${encodeURIComponent(
        lemma,
      )}/`,
    )
    .then((r) => r.data),

  /* -------------------------------------------------------------------------- */
  /*                       lemmatized_text.LemmatizedText                       */
  /* -------------------------------------------------------------------------- */
  lemmatizedText_cancel: (id) => axios.post(`${BASE_URL}lemmatized_texts/${id}/cancel/`),
  lemmatizedText_clone: (id) => axios.post(`${BASE_URL}lemmatized_texts/${id}/clone/`),
  lemmatizedText_fetch: (id) => axios.get(`${BASE_URL}lemmatized_texts/${id}/detail/`),
  lemmatizedText_fetchStatus: (id) => axios.get(`${BASE_URL}lemmatized_texts/${id}/status/`),
  lemmatizedText_fetchTokens: (id, vocabList, personalVocabList) => {
    if (!vocabList && !personalVocabList) {
      return axios.get(`${BASE_URL}lemmatized_texts/${id}/`);
    }
    let qs = '';
    if (vocabList) {
      qs = `vocablist_id=${vocabList}`;
    }
    if (personalVocabList) {
      qs = `personalvocablist=${personalVocabList}`;
    }
    return axios.get(`${BASE_URL}lemmatized_texts/${id}/?${qs}`);
  },
  lemmatizedText_fetchTokenHistory: (id, tokenIndex) => axios.get(
    `${BASE_URL}lemmatized_texts/${id}/tokens/${tokenIndex}/history/`,
  ),
  lemmatizedText_list: () => axios.get(`${BASE_URL}lemmatized_texts/`),
  lemmatizedText_retry: (id) => axios.post(`${BASE_URL}lemmatized_texts/${id}/retry/`),
  lemmatizedText_updateToken: (
    id,
    tokenIndex,
    resolved,
    vocabList,
    lemmaId = null,
    glossIds = [],
    lemma = null,
  ) => {
    if (vocabList === null) {
      return axios.post(`${BASE_URL}lemmatized_texts/${id}/`, {
        tokenIndex,
        lemmaId,
        glossIds,
        lemma,
        resolved,
      });
    }
    return axios.post(
      `${BASE_URL}lemmatized_texts/${id}/?vocablist_id=${vocabList}`,
      {
        tokenIndex,
        lemmaId,
        glossIds,
        lemma,
        resolved,
      },
    );
  },

  /* -------------------------------------------------------------------------- */
  /*                   lemmatized_text.LemmatizedTextBookmark                   */
  /* -------------------------------------------------------------------------- */
  bookmark_create: (textId) => axios.post(`${BASE_URL}bookmarks/`, { textId }),
  bookmark_delete: (bookmarkId) => axios.delete(`${BASE_URL}bookmarks/${bookmarkId}/`),
  bookmark_list: () => axios.get(`${BASE_URL}bookmarks/`),
  bookmark_fetch: (bookmarkId) => axios.get(`${BASE_URL}bookmarks/${bookmarkId}/`),
  bookmark_read_update: (bookmarkId, readStatus, flag) => axios.post(`${BASE_URL}bookmarks/${bookmarkId}/`, { readStatus, flag }),
  // bookmark_started_read_at: (bookmarkId) => axios.post(`${BASE_URL}bookmarks/${bookmarkId}/startedread/`),

  /* -------------------------------------------------------------------------- */
  /*                      vocab_list.PersonalVocabularyList                     */
  /* -------------------------------------------------------------------------- */
  personalVocabularyList_fetch: (lang) => axios.get(`${BASE_URL}personal_vocab_list/?lang=${lang}`),
  personalVocabularyList_fetchLangList: () => axios.get(`${BASE_URL}personal_vocab_list/quick_add/`),
  personalVocabularyList_update: (
    textId,
    lemmaId,
    familiarity,
    headword,
    definition,
    entryId,
    lang,
  ) => {
    let data = {
      familiarity,
      headword,
      definition,
      lemmaId,
    };
    if (lang !== null && entryId !== null) {
      return axios
        .post(`${BASE_URL}personal_vocab_list/${entryId}/?lang=${lang}`, data)
        .then((r) => r.data)
        .catch((error) => error);
    }
    if (entryId !== null) {
      return axios
        .post(`${BASE_URL}personal_vocab_list/${entryId}/?text=${textId}`, data)
        .then((r) => r.data)
        .catch((error) => error);
    }
    data = { ...data, lemmaId };
    return axios
      .post(`${BASE_URL}personal_vocab_list/?text=${textId}`, data)
      .then((r) => r.data)
      .catch((error) => error);
  },

  /* -------------------------------------------------------------------------- */
  /*                   vocab_list.PersonalVocabularyListEntry                   */
  /* -------------------------------------------------------------------------- */
  personalVocabularyListEntry_create: (
    headword,
    definition,
    vocabularyListId,
    familiarity,
    lang,
    lemmaId,
  ) => {
    const payload = {
      headword,
      definition,
      familiarity,
      // Django doesnt pick up key:value pairs with undefined values
      vocabulary_list_id: vocabularyListId || null,
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
  vocabularyListEntry_create: (
    vocabularyListId,
    headword,
    definition,
    lemmaId,
  ) => {
    const payload = {
      headword,
      definition,
    };
    if (lemmaId) {
      payload.lemma_id = lemmaId;
    }
    return axios.post(
      `${BASE_URL}vocab_lists/${vocabularyListId}/entries/`,
      payload,
    );
  },
  vocabularyListEntry_delete: (id) => axios.post(`${BASE_URL}vocab_entries/${id}/delete/`),
  vocabularyListEntry_link: (id, lemmaId) => axios.post(`${BASE_URL}vocab_entries/${id}/link/`, { lemma_id: lemmaId }),
  vocabularyListEntry_list: (id, cb) => axios.get(`${BASE_URL}vocab_lists/${id}/entries/`).then((r) => cb(r.data)),
  vocabularyListEntry_update: (id, headword, definition) => axios.post(`${BASE_URL}vocab_entries/${id}/edit/`, {
    headword,
    definition,
  }),

  /* -------------------------------------------------------------------------- */
  /*                            Not accessing a model                           */
  /* -------------------------------------------------------------------------- */
  supportedLangList_fetch: () => axios.get(`${BASE_URL}supported_languages/`),

  /* -------------------------------------------------------------------------- */
  /*         TODO: Delete these things, ensuring that they are not used.        */
  /* -------------------------------------------------------------------------- */
  fetchNode: (id, cb) => axios.get(`/lattices/${id}.json`).then((r) => cb(r.data)),
  fetchLatticeNodes: (headword, lang, cb) => axios
    .get(`${BASE_URL}lattice_nodes/?headword=${headword}&lang=${lang}`)
    .then((r) => cb(r.data)),
};
