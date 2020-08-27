<template>
  <div class="lattice-tree">
    <h4>{{ selectedToken.word }}</h4>
    <LatticeNode :node="selectedNode" @selected="onSelect" :show-ids="showIds" />
    <AddLemma @addLemma="onAddLemma" />
    <div class="text-right my-1"><small><a href @click.prevent="showIds = !showIds">Toggle Node IDs</a></small></div>

    <MarkResolved />
  </div>
</template>
<script>
  import AddLemma from './AddLemma.vue';
  import LatticeNode from './LatticeNode.vue';
  import MarkResolved from './MarkResolved.vue';
  import { UPDATE_TOKEN, ADD_LEMMA, RESOLVED_MANUAL } from '../constants';

  export default {
    components: { AddLemma, LatticeNode, MarkResolved },
    data() {
      return {
        showIds: false,
      };
    },
    computed: {
      textId() {
        return this.$store.state.textId;
      },
      selectedNode() {
        return this.selectedToken && this.$store.state.nodes[this.selectedToken.node];
      },
      selectedToken() {
        return this.$store.state.selectedToken;
      },
    },
    methods: {
      onAddLemma({ lemma }) {
        this.$store.dispatch(ADD_LEMMA, {
          id: this.textId,
          tokenIndex: this.selectedToken.tokenIndex,
          lemma,
          resolved: this.selectedToken.resolved,
        });
      },
      onSelect(node) {
        this.$store.dispatch(UPDATE_TOKEN, {
          id: this.textId,
          tokenIndex: this.selectedToken.tokenIndex,
          nodeId: node.pk,
          resolved: RESOLVED_MANUAL,
        });
      },
    },
  };
</script>
