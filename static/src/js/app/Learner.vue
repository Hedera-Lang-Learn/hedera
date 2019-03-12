<template>
  <div class="app-container">
    <div class="row">
      <div class="col-8">
        <LemmatizedText />
      </div>
      <div class="col-4">
        <div class="mb-5">
          <PersonalVocabList v-if="personalVocabList" :vocab-list="personalVocabList" />
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { FETCH_TOKENS, FETCH_PERSONAL_VOCAB_LIST, FETCH_TEXT } from './constants';

import LatticeTree from './modules/LatticeTree.vue';
import LemmatizedText from './modules/LemmatizedText.vue';
import PersonalVocabList from './modules/PersonalVocabList.vue';

export default {
  props: ["textId"],
  components: { LatticeTree, LemmatizedText, PersonalVocabList },
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
  }
}
</script>
