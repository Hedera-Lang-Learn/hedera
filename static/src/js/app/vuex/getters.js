export default {
  knownVocab: (state) => {
    const tokens = state.tokens.filter(t => t.word === t.word.toLowerCase());
    const totalTokens = tokens.filter(t => t.resolved !== 'na').length;
    const knownTokens = tokens.filter(t => t.inVocabList).length;
    return knownTokens / totalTokens;
  },
  selectedToken: (state) => {
    if (state.selectedIndex !== null && state.tokens.length > 0) {
      return state.tokens[state.selectedIndex];
    }
    return null;
  },
};
