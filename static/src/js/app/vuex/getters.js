export default {
  knownVocab: (state) => {
    const totalTokens = state.tokens.length;
    const knownTokens = state.tokens.filter(t => t.inVocabList).length;
    return knownTokens / totalTokens;
  },
  selectedToken: (state) => {
    if (state.selectedIndex !== null && state.tokens.length > 0) {
      return state.tokens[state.selectedIndex];
    }
    return null;
  },
};
