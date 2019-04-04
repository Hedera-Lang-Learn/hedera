<template>
  <div class="app-container">
    <div class="row">
      <div class="col-8">
        <LemmatizedText
          :vocab-entries="personalVocabList && personalVocabList.entries"
          :show-familiarity="showFamiliarity"
          @setRating="onSetRating"
        />
      </div>
      <div class="col-4">
        <div class="xxxposition-fixed">
          <div class="mb-5">
            <div class="text-stats">
              <div class="total-tokens">
                {{ tokens.length }}
                <div class="title">Total Tokens</div>
              </div>
              <div class="unique-tokens">
                {{ uniqueNodes.length }}
                <div class="title">Unique Tokens</div>
              </div>
            </div>
            <TextFamiliarity v-if="ranks" :ranks="ranks" />
            <VocabularyEntries class="at-root" :vocabEntries="vocabEntries" />
            <FamiliarityRating v-if="selectedNode && vocabEntries.length > 0" :value="selectedNodeRating" @input="onRatingChange" />
          </div>
          <div>
            <a href @click.prevent="toggleFamiliarity">{{ showFamiliarity ? 'Hide' : 'Show' }} Familiarity</a>
          </div>
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
import TextFamiliarity from './modules/TextFamiliarity.vue';

export default {
  props: ["textId"],
  components: { FamiliarityRating, LemmatizedText, VocabularyEntries, TextFamiliarity },
  data() {
    return {
      selectedNodeRating: null,
      showFamiliarity: false,
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
    toggleFamiliarity() {
      this.showFamiliarity = !this.showFamiliarity;
    },
    onRatingChange(rating) {
      const headword = (this.vocabEntries && this.vocabEntries[0] && this.vocabEntries[0].headword) || '';

      if (headword === '') {
        return;
      }

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
    },
    onSetRating({ rating, token }) {
      if (this.selectedNode) {
        this.onRatingChange(rating);
      } else {
        console.info('You need to select a node to rate with keystrokes.');
      }
    }
  },
  computed: {
    uniqueNodes() {
      return  [...new Set(this.tokens.map(token => token.node))];
    },
    ranks() {
      const familiarities = {unranked: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0};
      if (this.personalVocabList) {
        const rankedNodes = this.personalVocabList.entries.map(entry => entry.node);
        familiarities.unranked = this.uniqueNodes.filter(nodeId => rankedNodes.indexOf(nodeId) === -1).length;
        this.personalVocabList.entries.forEach(entry => familiarities[entry.familiarity] += 1);
        return Object.keys(familiarities).reduce((map, familiarity) => {
          map[familiarity] = 100 * (familiarities[familiarity] / this.uniqueNodes.length);
          return map;
        }, {});
      }
    },
    tokens() {
      return this.$store.state.tokens;
    },
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

<style lang="scss">
.vocab-entries.at-root {
  padding: 0;
  margin-bottom: 20px;

  .vocab-entry > span {
    display: block;
    &.headword {
      font-size: 1rem;
    }
  }
}

.text-stats {
  display: flex;
  justify-content: space-around;
  text-align: center;
  font-size: 30px;
  font-weight: bold;
  margin-bottom: 20px;

  .title {
    font-size: 18px;
    font-weight: normal;
  }
}
</style>

