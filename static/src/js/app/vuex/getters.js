export default {
  knownVocab: (state) => {
    const tokens = state.tokens.filter((t) => t.word === t.word.toLowerCase());
    const totalTokens = tokens.filter((t) => t.resolved !== 'na').length;
    const knownTokens = tokens.filter((t) => t.inVocabList).length;
    return knownTokens / totalTokens;
  },
  weightedKnownVocab: (state) => {
    const tokens = state.tokens.filter((t) => t.word === t.word.toLowerCase());

    // Create a set of unique tokens
    const uniqueTokens = new Set();
    for (let i = 0; i < tokens.length; i += 1) {
      if (tokens[i].resolved !== 'na') {
        if (tokens[i].label) {
          // Looks like 'label' stores the lemma
          uniqueTokens.add(tokens[i].label);
        } else {
          // If there is no lemma, use the word as is
          uniqueTokens.add(tokens[i].word);
        }
      }
    }

    // Determine which tokens in the set of unique tokens are known,
    // and put them in a new set
    const knownUniqueTokens = new Set();
    for (let i = 0; i < tokens.length; i += 1) {
      if (tokens[i].inVocabList) {
        knownUniqueTokens.add(tokens[i].label);
      }
    }

    const totalUniqueTokens = uniqueTokens.size;
    const totalKnownUniqueTokens = knownUniqueTokens.size;
    // Return proportion of known unique tokens, which is equivalent to weighted percentage
    return totalKnownUniqueTokens / totalUniqueTokens;
  },
  selectedToken: (state) => {
    if (state.selectedIndex !== null && state.tokens.length > 0) {
      return state.tokens[state.selectedIndex];
    }
    return null;
  },
};
