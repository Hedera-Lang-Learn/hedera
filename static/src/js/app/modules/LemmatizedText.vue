<template>
  <div class="lemmatized-text">
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
import { SELECT_TOKEN, FETCH_NODE } from "../constants";

import Token from "./Token.vue";

export default {
  components: { Token },
  methods: {
    onToggleSelect({ token, index }) {
      if (this.selectedIndex === index && this.selectedToken === token) {
        this.$store.dispatch(SELECT_TOKEN, { token: null, index: null });
      } else {
        this.$store.dispatch(SELECT_TOKEN, { token, index });
        if (token.node !== null) {
          this.$store.dispatch(FETCH_NODE, { id: token.node });
        }
      }
    }
  },
  computed: {
    tokens() {
      return this.$store.state.tokens;
    },
    selectedIndex() {
      return this.$store.state.selectedIndex;
    },
    selectedToken() {
      return this.$store.state.selectedToken;
    }
  }
};
</script>
