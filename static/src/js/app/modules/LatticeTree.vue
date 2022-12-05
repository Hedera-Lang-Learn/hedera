<template>
  <div class="lattice-tree">
    <h4>{{ selectedToken.word }}</h4>
    <LatticeNode :lemma="selectedLemma" @selected="onSelect" :show-ids="showIds" />
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
  import { LEMMATIZED_TEXT_UPDATE_TOKEN, LEMMA_CREATE, RESOLVED_MANUAL } from '../constants';

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
      selectedLemma() {
        return this.selectedToken && this.$store.state.lemmas[this.selectedToken.lemma_id];
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
        this.$store.dispatch(LEMMA_CREATE, {
          id: this.textId,
          tokenIndex: this.selectedToken.tokenIndex,
          lemma,
          resolved: this.selectedToken.resolved,
        });
      },
      onSelect(node) {
        this.$store.dispatch(LEMMATIZED_TEXT_UPDATE_TOKEN, {
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
