const testData = {
  forms: {
    sum: {
      lang: 'lat',
      form: 'sum',
      lemmas: [
        {
          pk: 1225,
          lemma: 'sum',
          alt_lemma: 'sum1',
          label: 'sum, esse, fuī',
          rank: 1,
          glosses: [{ pk: 81965, gloss: 'to be, exist, live' }],
        },
      ],
    },
  },
  supportedLanguages: [
    ['lat', 'Latin'],
    // ['grc', 'Ancient Greek'],
    // ['rus', 'Russian']
  ],
  personalVocabList: {
    entries: [
      {
        id: 366,
        headword: 'cum',
        definition:
          'with, together with, in the company of, in connection with, along with, together, and',
        familiarity: 1,
        lemma_id: 1260,
        lemma: 'cum',
      },
      {
        id: 367,
        headword: 'filia',
        definition: 'a daughter',
        familiarity: 1,
        lemma_id: 20526,
        lemma: 'filia',
      },
      {
        id: 365,
        headword: 'sum',
        definition: 'to be, exist, live',
        familiarity: 1,
        lemma_id: 1225,
        lemma: 'sum',
      },
    ],
  },
};

export default testData;
