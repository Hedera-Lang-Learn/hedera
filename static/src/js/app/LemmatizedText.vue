<template>
  <div class="lemmatized-text">
    <h1>Lemmatized Text</h1>

    <div class="text text-lg">
      <span
        v-for="(item, index) in items" :key="index"
        class="token" :class="{unresolved: !item.resolved, selected: selectedToken === item}"
        @click.prevent="onClick(item, index)"
      >{{ item.token }} </span>
    </div>
  </div>
</template>
<script>
import { SELECT_TOKEN, FETCH_NODE } from './constants';

export default {
  methods: {
      onClick(item, index) {
          this.$store.dispatch(SELECT_TOKEN, { token: item, index });
          this.$store.dispatch(FETCH_NODE, { id: item.node });
      }
  },
  computed: {
    items() {
      return this.$store.state.texts;
    },
    selectedToken() {
      return this.$store.state.selectedToken;
    }
  }
};
</script>
