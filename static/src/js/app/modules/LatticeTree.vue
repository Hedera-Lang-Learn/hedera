<template>
  <div class="lattice-tree">
    <h4>{{ token.token }}</h4>
    <AddLemma @addLemma="onAddLemma" />
    <LatticeNode :node="node" @selected="onSelect" />
    <MarkResolved :resolved="token.resolved" @toggle="markResolved" />
  </div>
</template>
<script>
import AddLemma from './AddLemma.vue';
import LatticeNode from "./LatticeNode.vue";
import MarkResolved from './MarkResolved.vue';
import { UPDATE_TOKEN, ADD_LEMMA } from "../constants";

export default {
  props: ["token", "index", "node"],
  components: { AddLemma, LatticeNode, MarkResolved },
  computed: {
    textId() {
      return this.$store.state.textId;
    }
  },
  methods: {
    onAddLemma({ lemma }) {
      this.$store.dispatch(ADD_LEMMA, {
        id: this.textId,
        tokenIndex: this.index,
        lemma,
        resolved: this.token.resolved,
      });
    },
    onSelect(node) {
      this.$store.dispatch(UPDATE_TOKEN, {
        id: this.textId,
        tokenIndex: this.index,
        nodeId: node.pk,
        resolved: this.token.resolved
      });
    },
    markResolved({ resolved }) {
      this.$store.dispatch(UPDATE_TOKEN, {
        id: this.textId,
        tokenIndex: this.index,
        nodeId: this.node ? this.node.pk : null,
        resolved
      });
    }
  }
};
</script>
