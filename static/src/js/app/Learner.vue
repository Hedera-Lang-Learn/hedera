<template>
  <div class="app-container">
    <div class="row">
      <div class="col-8">
        <LemmatizedText />
      </div>
      <div class="col-4">
        <div class="mb-5">
          <PersonalVocabList v-if="personalVocabList" :vocab-list="personalVocabList" />
          <VocabularyEntries :vocabEntries="vocabEntries" />
          <div> <!-- make own component -->
            <div class="likert-group">
              <span class="">x</span>
              <span class="">x</span>
              <span class="">x</span>
              <span class="">x</span>
              <span class="">x</span>
            </div>
            <div class="help-text"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { FETCH_TOKENS, FETCH_PERSONAL_VOCAB_LIST, FETCH_TEXT } from './constants';

import LemmatizedText from './modules/LemmatizedText.vue';
import PersonalVocabList from './modules/PersonalVocabList.vue';
import VocabularyEntries from './modules/VocabularyEntries.vue';

export default {
  props: ["textId"],
  components: { LemmatizedText, PersonalVocabList, VocabularyEntries },
  watch: {
    textId: {
      immediate: true,
      handler() {
        this.$store.dispatch(FETCH_TEXT, { id: this.textId }).then(() => this.$store.dispatch(FETCH_PERSONAL_VOCAB_LIST));
      }
    },
    selectedVocabList: {
      immediate: true,
      handler() {
        this.$store.dispatch(FETCH_TOKENS, { id: this.textId, personalVocabList: this.selectedVocabList });
      }
    }
  },
  computed: {
    personalVocabList() {
      return this.$store.state.personalVocabList;
    },
    vocabEntries() {
      return this.selectedNode && this.selectedNode.vocabulary_entries;
    },
    selectedToken() {
      return this.$store.getters.selectedToken;
    },
    selectedNode() {
      return this.selectedToken && this.$store.state.nodes[this.selectedToken.node];
    }
  }
}
</script>
