<template>
  <div class="app-container">
    <div class="row">
      <div class="col-8">
        <LemmatizedText />
      </div>
      <div class="col-4">
        <div class="mb-5">
          <VocabularyEntries :vocabEntries="vocabEntries" />
          <FamiliarityRating v-if="selectedNode" :value="selectedNodeRating" @input="onRatingChange" />
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { FETCH_TOKENS, FETCH_PERSONAL_VOCAB_LIST, FETCH_TEXT, CREATE_VOCAB_ENTRY, UPDATE_VOCAB_ENTRY } from './constants';

import LemmatizedText from './modules/LemmatizedText.vue';
import VocabularyEntries from './modules/VocabularyEntries.vue';
import FamiliarityRating from './modules/FamiliarityRating.vue';

export default {
  props: ["textId"],
  components: { FamiliarityRating, LemmatizedText, VocabularyEntries },
  data() {
    return {
      selectedNodeRating: null,
    }
  },
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
    },
    selectedNode: {
      handler() {
        if (this.personalVocabEntry) {
          this.selectedNodeRating = this.personalVocabEntry.familiarity;
        } else {
          this.selectedNodeRating = null;
        }
      }
    },
  },
  methods: {
    onRatingChange(rating) {
      const headword = (this.vocabEntries && this.vocabEntries[0] && this.vocabEntries[0].headword) || '';
      const gloss = (this.vocabEntries && this.vocabEntries[0] && this.vocabEntries[0].gloss) || '';
      this.selectedNodeRating = rating;
      if (this.personalVocabEntry) {
        this.$store.dispatch(UPDATE_VOCAB_ENTRY, {
          entryId: this.personalVocabEntry.id,
          familiarity: rating,
          headword,
          gloss,
        });
      } else {
        this.$store.dispatch(CREATE_VOCAB_ENTRY, {
          nodeId: this.selectedNode.pk,
          familiarity: rating,
          headword,
          gloss,
        });
      }
    }
  },
  computed: {
    personalVocabList() {
      return this.$store.state.personalVocabList;
    },
    personalVocabEntry() {
      return this.selectedNode && this.personalVocabList && this.personalVocabList.entries && this.personalVocabList.entries.filter(e => {
        return e.node === this.selectedNode.pk
      })[0];
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
