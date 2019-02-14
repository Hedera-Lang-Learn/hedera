<template>
  <div class="app-container">
    <nav><a href="/lemmatized_text/">Lemmatized Texts</a></nav>

    <div class="row">
      <div class="col-8">
        <router-view />
      </div>
      <div class="col-4">
        <LatticeTree v-if="selectedToken" :node="selectedNode" :index="selectedIndex" :token="selectedToken" />
      </div>
    </div>
  </div>
</template>
<script>
import LatticeTree from './LatticeTree.vue';
import { FETCH_TOKENS } from './constants';

export default {
  components: { LatticeTree },
  created() {
    this.$store.dispatch(FETCH_TOKENS, { id: this.$route.params.id });
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
