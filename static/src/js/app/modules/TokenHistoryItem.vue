<template>
  <div class="token-history-item">
    <div class="node">
      <span class="lattice-label">{{ node.label }}</span>
      <span class="lattice-gloss">{{ node.gloss }}</span>
    </div>
    <div class="meta">
      <div class="who">{{ item.user }}</div>
      <div class="when">{{ when }}</div>
    </div>
  </div>
</template>

<script>
  import { FETCH_NODE } from '../constants';

  export default {
    props: ['item'],
    created() {
      if (this.node === undefined) {
        this.$store.dispatch(FETCH_NODE, { id: this.item.node });
      }
    },
    computed: {
      node() {
        return this.$store.state.nodes[this.item.node];
      },
      when() {
        return new Date(this.item.createdAt).toLocaleString('en-US');
      },
    },
  };
</script>

<style lang="scss" scoped>
  @import "../../../scss/config";
  .token-history-item .meta {
    display: flex;
    justify-content: space-between;
    font-size: 10pt;
    color: $gray-500;
  }
  .token-history-item {
    padding: 0.375rem 0.5rem 0.5rem;
    border-bottom: 1px solid $gray-300;
    border-right: 1px solid $gray-300;
    border-left: 1px solid $gray-300;
  }
  .token-history-item:first-child {
    margin-top: 1rem;
    border-top: 1px solid $gray-300;
  }
</style>
