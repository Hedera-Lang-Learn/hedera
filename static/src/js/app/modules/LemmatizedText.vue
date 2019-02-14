<template>
  <div class="lemmatized-text">
    <Token v-for="(token, index) in tokens" :key="index"
      :token="token"
      :index="index"
      :selected="selectedIndex === index"
      @selected="onSelect" />
  </div>
</template>
<script>
import { SELECT_TOKEN, FETCH_NODE } from '../constants';

import Token from './Token.vue';

export default {
  components: { Token },
  methods: {
      onSelect({token, index}) {
          this.$store.dispatch(SELECT_TOKEN, { token, index });
          if (token.node !== null) {
            this.$store.dispatch(FETCH_NODE, { id: token.node });
          }
      }
  },
  computed: {
    tokens() {
      return this.$store.state.tokens;
    },
    selectedIndex() {
      return this.$store.state.selectedIndex;
    }
  }
};
</script>
