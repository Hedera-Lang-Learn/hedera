<template>
  <div class="lemmatized-text" :class="highlightClass">
    <template v-for="(token, index) in tokens">
      <Token
        :key="index"
        :token="token"
        :index="index"
        :selected-token="selectedToken"
        :selected-index="selectedIndex"
        :same-words="sameWords"
        :class="familiarityClass(token)"
        @toggleSelected="onToggleSelect"
      />
    </template>
  </div>
</template>
<script>
  import debounce from 'lodash.debounce';
  import { SELECT_TOKEN, FETCH_NODE } from '../constants';

  import Token from './Token.vue';

  const prevIndex = (currentIndex, tokens) => {
    let index = currentIndex - 1;
    if (index === -1) {
      index = tokens.length - 1;
    }
    return index;
  };

  const nextIndex = (currentIndex, tokens) => {
    let index = currentIndex + 1;
    if (index === tokens.length) {
      index = 0;
    }
    return index;
  };

  export default {
    props: ['showFamiliarity', 'vocabEntries'],
    components: { Token },
    shortcuts: {
      prevWord() {
        this.goToWord(prevIndex);
      },
      nextWord() {
        this.goToWord(nextIndex);
      },
      prevUnresolved() {
        this.goToUnresolved(prevIndex);
      },
      nextUnresolved() {
        this.goToUnresolved(nextIndex);
      },
      one() {
        this.$emit('setRating', { rating: 1, token: this.selectedToken });
      },
      two() {
        this.$emit('setRating', { rating: 2, token: this.selectedToken });
      },
      three() {
        this.$emit('setRating', { rating: 3, token: this.selectedToken });
      },
      four() {
        this.$emit('setRating', { rating: 4, token: this.selectedToken });
      },
      five() {
        this.$emit('setRating', { rating: 5, token: this.selectedToken });
      },
    },
    methods: {
      selectToken(index) {
        const fetchNode = () => {
          if (this.selectedToken.node !== null) {
            this.$store.dispatch(FETCH_NODE, { id: this.selectedToken.node });
          }
        };
        const debouncedFetchNode = debounce(fetchNode, 300);

        // The debounce is delaying the call but it's accumulating all the instances
        // so the network call is happening multiple times.
        this.$store.dispatch(SELECT_TOKEN, { index })
          .then(debouncedFetchNode());
      },
      onToggleSelect({ token, index }) {
        if (this.selectedIndex === index && this.selectedToken === token) {
          this.$store.dispatch(SELECT_TOKEN, { index: null });
        } else {
          this.selectToken(index);
        }
      },
      goToWord(indexFunction) {
        let index = 0;
        if (this.selectedIndex !== null) {
          index = indexFunction(this.selectedIndex, this.tokens);
        }
        this.selectToken(index);
      },
      goToUnresolved(indexFunction) {
        let index = 0;
        if (this.selectedIndex !== null) {
          const unresolvedTokenIndex = indexFunction(
            this.unresolvedTokens.indexOf(this.selectedToken),
            this.unresolvedTokens,
          );
          const token = this.unresolvedTokens[unresolvedTokenIndex];
          index = this.tokens.indexOf(token);
        }
        this.selectToken(index);
      },
      familiarityClass(token) {
        let className = '';
        if (this.showFamiliarity && this.vocabEntries) {
          const entries = this.vocabEntries.reduce((map, obj) => {
            map[obj.node] = obj.familiarity;
            return map;
          }, {});
          className = entries[token.node] !== undefined ? `rating-${entries[token.node]}` : '';
        }
        return className;
      },
    },
    computed: {
      unresolvedTokens() {
        return this.tokens.filter((t) => !t.resolved || t === this.selectedToken);
      },
      highlightClass() {
        if (this.$store.state.selectedVocabList === null) {
          return '';
        }
        return this.showInVocabList ? 'highlight-in-list' : 'highlight-not-in-list';
      },
      showInVocabList() {
        return this.$store.state.showInVocabList;
      },
      tokens() {
        return this.$store.state.tokens;
      },
      selectedIndex() {
        return this.$store.state.selectedIndex;
      },
      selectedToken() {
        return this.$store.getters.selectedToken;
      },
      sameWords() {
        return this.tokens.filter((t) => this.selectedToken && t.word === this.selectedToken.word);
      },
    },
  };
</script>

<style lang="scss">
@import "../../../scss/config";
  .lemmatized-text {
    .token.rating-1 {
      color: $rating-1;
    }
    .token.rating-2 {
      color: $rating-2;
    }
    .token.rating-3 {
      color: $rating-3;
    }
    .token.rating-4 {
      color: $rating-4;
    }
    .token.rating-5 {
      color: $rating-5;
    }
  }
</style>
