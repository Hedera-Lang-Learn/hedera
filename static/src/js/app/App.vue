<template>
  <div class="app-container">
    <div class="row">
      <div class="col-8">
        <LemmatizedText />
      </div>
      <div class="col-4">
        <div class="">
          <VocabList @selected="onVocabListSelect" v-for="vlist in vocabLists" :key="vlist.id" :vocab-list="vlist" />
        </div>
        <LatticeTree v-if="selectedToken" :node="selectedNode" :index="selectedIndex" :token="selectedToken" />
      </div>
    </div>
  </div>
</template>
<script>
import { FETCH_TOKENS, FETCH_VOCAB_LISTS, SELECT_VOCAB_LIST } from './constants';

import LatticeTree from './modules/LatticeTree.vue';
import LemmatizedText from './modules/LemmatizedText.vue';
import VocabList from './modules/VocabList.vue';

export default {
  props: ["textId"],
  components: { LatticeTree, LemmatizedText, VocabList },
  created() {
    this.$store.dispatch(FETCH_VOCAB_LISTS);
  },
  methods: {
    onVocabListSelect(id) {
      this.$store.dispatch(SELECT_VOCAB_LIST, id);
    }
  },
  watch: {
    selectedVocabList: {
      immediate: true,
      handler() {
        this.$store.dispatch(FETCH_TOKENS, { id: this.textId, vocabList: this.selectedVocabList });
      }
    }
  },
  computed: {
    selectedVocabList() {
      return this.$store.state.selectedVocabList;
    },
    vocabLists() {
      return this.$store.state.vocabLists;
    },
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
