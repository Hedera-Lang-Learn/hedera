<template>
  <div class="lemmatized-text" :class="highlightClass">
    <template v-for="(token, index) in tokens">
      <Token
        :key="index"
        :token="token"
        :index="index"
        :selected="selectedIndex === index"
        @toggleSelected="onToggleSelect"
      />
      {{ ' ' }}
    </template>
  </div>
</template>
<script>
import debounce from 'lodash.debounce';
import { SELECT_TOKEN, FETCH_NODE } from "../constants";

import Token from "./Token.vue";

export default {
  components: { Token },
  shortcuts: {
    prevWord() {
      let index = 0;
      if (this.selectedIndex !== null) {
        index = this.selectedIndex - 1;
        if (index === -1) {
          index = this.tokens.length - 1;
        }
      }
      this.selectToken(index);
    },
    nextWord() {
      let index = 0;
      if (this.selectedIndex !== null) {
        index = this.selectedIndex + 1;
        if (index === this.tokens.length) {
          index = 0;
        }
      }
      this.selectToken(index);
    }
  },
  methods: {
    selectToken(index) {
      const fetchNode = () => {
        if (this.selectedToken.node !== null) {
          this.$store.dispatch(FETCH_NODE, { id: this.selectedToken.node });
        }
      }
      const debouncedFetchNode = debounce(fetchNode, 300);

      // The debounce is delaying the call but it's accumulating all the instances
      // so the network call is happening multiple times.
      this.$store.dispatch(SELECT_TOKEN, { index });
      debouncedFetchNode();
    },
    onToggleSelect({ index }) {
      if (this.selectedIndex === index && this.selectedToken === token) {
        this.$store.dispatch(SELECT_TOKEN, { index: null });
      } else {
        this.selectToken(index);
      }
    }
  },
  computed: {
    highlightClass() {
      if (this.$store.state.selectedVocabList === null) {
        return '';
      }
      return this.showInVocabList ? 'highlight-in-list' : 'highlight-not-in-list'
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
    }
  }
};
</script>
