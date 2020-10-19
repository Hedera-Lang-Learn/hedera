<template>
  <div class="lattice-tree cloning" v-if="cloning">
    <p>Cloning...</p>
    <small>You will be redirected to your clone when complete.</small>
  </div>
  <div class="lattice-tree clone-required" v-else-if="requireClone">
    <div class="well">
      This text currently belongs to one or more classes.  You must clone it if
      you want to make changes to it's lemma lattice.
    </div>
    <button class="btn btn-block btn-primary" @click.prevent="onCloneText">Clone Now</button>
  </div>
  <div class="lattice-tree" v-else>
    <h4>{{ selectedToken.word }}</h4>
    <LatticeNode :node="selectedNode" @selected="onSelect" :show-ids="showIds" />
    <AddLemma @addLemma="onAddLemma" v-if="false" />
    <div v-if="showToggle" class="text-right my-1"><small><a href @click.prevent="toggleShowIds = !toggleShowIds">Toggle Node IDs</a></small></div>

    <MarkResolved />

    <TokenHistory />
  </div>
</template>
<script>
  import AddLemma from './AddLemma.vue';
  import LatticeNode from './LatticeNode.vue';
  import MarkResolved from './MarkResolved.vue';
  import TokenHistory from './TokenHistory.vue';

  import api from '../api';
  import { UPDATE_TOKEN, ADD_LEMMA, RESOLVED_MANUAL } from '../constants';

  export default {
    components: {
      AddLemma,
      LatticeNode,
      MarkResolved,
      TokenHistory,
    },
    data() {
      return {
        toggleShowIds: false,
        cloning: false,
        clonedTextId: null,
      };
    },
    computed: {
      showToggle() {
        return this.$store.state.me.showNodeIds === 'toggle';
      },
      showIds() {
        const { showNodeIds } = this.$store.state.me;
        return showNodeIds === 'always'
          || (showNodeIds === 'toggle' && this.toggleShowIds);
      },
      textId() {
        return this.$store.state.textId;
      },
      selectedNode() {
        return this.selectedToken && this.$store.state.nodes[this.selectedToken.node];
      },
      selectedToken() {
        return this.$store.state.selectedToken;
      },
      requireClone() {
        return this.$store.state.text && this.$store.state.text.requireClone;
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
      onCloneText() {
        this.cloning = true;
        api.cloneText(this.textId, (data) => {
          window.location = data.data.detailUrl;
        });
      },
    },
  };
</script>

<style lang="scss" scoped>
  @import "../../../scss/config";

  .clone-required .well {
    background: $gray-100;
    border: 1px solid $gray-200;
    color: $gray-700;
    margin-bottom: 20px;
    padding: 10px 15px;
  }
</style>
