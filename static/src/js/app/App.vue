<template>
  <div class="app-container">
    <div class="row">
      <div class="col-8">
        <LemmatizedText />
      </div>
      <div class="col-4">
        <LatticeTree v-if="selectedToken" :node="selectedNode" :index="selectedIndex" :token="selectedToken" />
      </div>
    </div>
  </div>
</template>
<script>
import { FETCH_TOKENS } from './constants';

import LatticeTree from './modules/LatticeTree.vue';
import LemmatizedText from './modules/LemmatizedText.vue';

export default {
  props: ["textId"],
  components: { LatticeTree, LemmatizedText },
  created() {
    this.$store.dispatch(FETCH_TOKENS, { id: this.textId });
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
