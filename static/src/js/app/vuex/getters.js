export default {
  knownVocab: (state) => {
    const totalTokens = state.tokens.length;
    const knownTokens = state.tokens.filter(t => t.inVocabList).length;
    return knownTokens / totalTokens;
  }
};
