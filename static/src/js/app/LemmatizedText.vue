<template>
  <div class="lemmatized-text">
      <span
        v-for="(token, index) in tokens" :key="index"
        class="token" :class="{unresolved: !token.resolved, selected: selectedIndex === index, 'no-lemma': token.node === null }"
        @click.prevent="onClick(token, index)"
      >{{ token.token }} </span>
  </div>
</template>
<script>
import { SELECT_TOKEN, FETCH_NODE } from './constants';

export default {
  methods: {
      onClick(token, index) {
          this.$store.dispatch(SELECT_TOKEN, { token, index });
          this.$store.dispatch(FETCH_NODE, { id: token.node });
      }
  },
  computed: {
    tokens() {
      return this.$store.state.tokens;
    },
    selectedToken() {
      return this.$store.state.selectedToken;
    },
    selectedIndex() {
      return this.$store.state.selectedIndex;
    }
  }
};
</script>
