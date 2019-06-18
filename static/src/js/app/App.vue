<template>
  <div class="app-container">
    <div class="row">
      <div class="col-8">
        <LemmatizedText />
      </div>
      <div class="col-4">
        <div class="mb-5">
          <VocabList @toggleSelected="onVocabListToggle" v-for="vlist in vocabLists" :key="vlist.id" :vocab-list="vlist" />
        </div>
        <LatticeTree v-if="selectedToken" :node="selectedNode" :index="selectedIndex" :token="selectedToken" />
      </div>
    </div>
  </div>
</template>
<script>
import { FETCH_TOKENS, FETCH_VOCAB_LISTS, TOGGLE_VOCAB_LIST, FETCH_TEXT, FETCH_USER_ROLES } from './constants';

import LatticeTree from './modules/LatticeTree.vue';
import LemmatizedText from './modules/LemmatizedText.vue';
import VocabList from './modules/VocabList.vue';

export default {
  props: ["textId"],
  components: { LatticeTree, LemmatizedText, VocabList },
  methods: {
    onVocabListToggle(id) {
      this.$store.dispatch(TOGGLE_VOCAB_LIST, id);
    }
  },
  watch: {
    textId: {
      immediate: true,
      handler() {
        this.$store.dispatch(FETCH_TEXT, { id: this.textId }).then(() => this.$store.dispatch(FETCH_VOCAB_LISTS));
      }
    },
    selectedVocabList: {
      immediate: true,
      handler() {
        this.$store.dispatch(FETCH_TOKENS, { id: this.textId, vocabList: this.selectedVocabList });
      }
    }
  },
  created() {
    this.$store.dispatch(FETCH_USER_ROLES);
  },
  computed: {
    selectedVocabList() {
      return this.$store.state.selectedVocabList;
    },
    vocabLists() {
      return this.$store.state.vocabLists;
    },
    selectedToken() {
      return this.$store.getters.selectedToken;
    },
    selectedIndex() {
      return this.$store.state.selectedIndex;
    },
    selectedNode() {
      return this.selectedToken && this.$store.state.nodes[this.selectedToken.node];
    }
  }
}
</script>
