<template>
  <div class="app-container">
    <router-view />
    <aside v-if="selectedToken">
      <pre>{{ selectedToken }} @ {{ selectedIndex }}</pre>
      <pre>{{ selectedNode }}</pre>
    </aside>
  </div>
</template>
<script>
import { FETCH_ITEMS } from './constants';

export default {
  created() {
    this.$store.dispatch(FETCH_ITEMS, { id: this.$route.params.id });
  },
  computed: {
    selectedToken() {
      return this.$store.state.selectedToken;
    },
    selectedIndex() {
      return this.$store.state.selectedIndex;
    },
    selectedNode() {
      return this.$store.state.nodes[this.selectedToken.node];
    }
  }
}
</script>
