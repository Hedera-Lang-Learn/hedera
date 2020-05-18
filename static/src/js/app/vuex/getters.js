export default {
  knownVocab: (state) => {
    const tokens = state.tokens.filter((t) => t.word === t.word.toLowerCase());
    const totalTokens = tokens.filter((t) => t.resolved !== 'na').length;
    const knownTokens = tokens.filter((t) => t.inVocabList).length;
    return knownTokens / totalTokens;
  },
  sameWords: (state) => {
    const selected = state.selectedToken;
    return state.tokens.filter((t) => selected && t.word === selected.word);
  },
};
