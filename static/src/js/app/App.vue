<template>
  <div class="app-container">
    <div class="row">
      <div class="col-8">
        <LemmatizedText />
      </div>
      <div class="col-4">
        <VocabListSelect class="mb-5" :vocab-lists="vocabLists" />
        <LatticeTree v-if="selectedToken" />
      </div>
    </div>
  </div>
</template>
<script>
  import {
    FETCH_TOKENS,
    FETCH_VOCAB_LISTS,
    FETCH_TEXT,
    FETCH_ME,
  } from './constants';

  import LatticeTree from './modules/LatticeTree.vue';
  import LemmatizedText from './modules/LemmatizedText.vue';
  import VocabListSelect from './components/vocab-list-select';

  export default {
    props: ['textId'],
    components: { LatticeTree, LemmatizedText, VocabListSelect },
    created() {
      this.$store.dispatch(FETCH_ME);
    },
    watch: {
      textId: {
        immediate: true,
        handler() {
          this.$store.dispatch(FETCH_TEXT, { id: this.textId }).then(() => this.$store.dispatch(FETCH_VOCAB_LISTS));
        },
      },
      selectedVocabList: {
        immediate: true,
        handler() {
          this.$store.dispatch(FETCH_TOKENS, { id: this.textId, vocabList: this.selectedVocabList });
        },
      },
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
    },
  };
</script>
