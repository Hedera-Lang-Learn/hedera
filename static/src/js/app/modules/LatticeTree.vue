<template>
  <div class="lattice-tree">
    <h4>{{ token.token }}</h4>
    <LatticeNode :node="node" @selected="onSelect" />
    <MarkResolved :resolved="token.resolved" @toggle="markResolved" />
  </div>
</template>
<script>
import LatticeNode from "./LatticeNode.vue";
import MarkResolved from './MarkResolved.vue';
import { UPDATE_TOKEN } from "../constants";

export default {
  props: ["token", "index", "node"],
  components: { LatticeNode, MarkResolved },
  computed: {
    textId() {
      return this.$store.state.textId;
    }
  },
  methods: {
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
