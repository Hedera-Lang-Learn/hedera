<template>
  <div class="app-container" :class="{'read-mode': readMode}">
    <div class="row">
      <div class="col-8">
        <LemmatizedText
          :vocab-entries="personalVocabList && personalVocabList.entries"
          :show-familiarity="showFamiliarity"
          @setRating="onSetRating"
        />
      </div>
      <div class="col-4">
        <div class="read-mode-toggle">
          <label>Toggle Read Mode</label>
          <div class="btn-group">
            <button class="btn btn-outline-primary" :class="{active: readMode}" @click.prevent="readMode = true">On</button>
            <button class="btn btn-outline-primary" :class="{active: !readMode}" @click.prevent="readMode = false">Off</button>
          </div>
        </div>
        <div class="glosses" v-if="readMode">
          <h4>
            Glosses
            <a v-if="glossesDownload" :href="glossesDownload" download="glosses.csv">Export</a>
          </h4>
          <div class="glossed-token" v-for="gloss in glosses" :key="gloss.pk">
            <span class="token">{{ gloss.label }}</span>
            <span class="gloss">{{ gloss.gloss }}</span>
          </div>
        </div>
        <div class="xxxposition-fixed" v-else>
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
            <FamiliarityRating v-if="selectedNode" :value="selectedNodeRating" @input="onRatingChange" />
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

const toCSV = (data) => {
  if (data.length === 0) {
    return null;
  }

  let result, ctr;
  const columnDelimiter = ',';
  const lineDelimiter = '\n';
  const keys = Object.keys(data[0]);

  result = '';
  result += keys.join(columnDelimiter);
  result += lineDelimiter;

  data.forEach(item => {
      ctr = 0;
      keys.forEach(key => {
          if (ctr > 0) {
            result += columnDelimiter;
          }
          result += `"${item[key]}"`;
          ctr++;
      });
      result += lineDelimiter;
  });

  return result;
}

export default {
  props: ["textId"],
  components: { FamiliarityRating, LemmatizedText, VocabularyEntries, TextFamiliarity },
  data() {
    return {
      selectedNodeRating: null,
      showFamiliarity: false,
      readMode: false,
    }
  },
  watch: {
    textId: {
      immediate: true,
      handler() {
        this.$store.dispatch(FETCH_TEXT, { id: this.textId }).then(() => this.$store.dispatch(FETCH_PERSONAL_VOCAB_LIST, { lang: this.text.lang }));
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
      const { label, gloss } = this.selectedNode;

      this.selectedNodeRating = rating;
      if (this.personalVocabEntry) {
        this.$store.dispatch(UPDATE_VOCAB_ENTRY, {
          entryId: this.personalVocabEntry.id,
          familiarity: rating,
          headword: label,
          gloss,
        });
      } else {
        this.$store.dispatch(CREATE_VOCAB_ENTRY, {
          nodeId: this.selectedNode.pk,
          familiarity: rating,
          headword: label,
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
    text() {
      return this.$store.state.text;
    },
    uniqueNodes() {
      return  [...new Set(this.tokens.map(token => token.node))];
    },
    ranks() {
      return this.personalVocabList && this.personalVocabList.statsByText[this.$store.state.textId];
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
    },
    knownEntries() {
      return this.personalVocabList.entries.filter(e => e.familiarity > 2);
    },
    glosses() {
      return this.uniqueNodes
        .filter(node => this.knownEntries.filter(k => k.node === node).length === 0)
        .map(node => this.tokens.filter(t => t.node === node)[0] || null)
        .filter(t => t !== null && t.gloss !== null && t.resolved !== 'unresolved');
    },
    glossesDownload() {
      const data = toCSV(this.glosses.map(g => ({label: g.label, gloss: g.gloss})));
      if (data !== null) {
        return encodeURI(`data:text/csv;charset=utf-8,${data}`);
      }
    }
  }
}
</script>

<style lang="scss">
@import "../../scss/config";
.read-mode-toggle {
  text-align: center;
  label {
    display: block;
  }
  background: #EFEFEF;
  padding: 15px;
  margin-bottom: 25px;
  .btn-group {
    background: #FFF;
  }
}
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

.read-mode {
  .token {
    cursor: inherit;
  }
  .unresolved {
    font-weight: inherit;
  }
  .no-lemma,
  .lemmatized-text .token.rating-1,
  .lemmatized-text .token.rating-2,
  .lemmatized-text .token.rating-3,
  .lemmatized-text .token.rating-4,
  .lemmatized-text .token.rating-5 {
    color: inherit;
  }
  .sameNode {
    border: none;
  }

  .glosses {
    h4 {
      display: flex;
      justify-content: space-between;
      a {
        font-size: 12pt;
        font-weight: 400;
        margin-top: auto;
      }
    }
    .glossed-token {
      font-family: 'Noto Serif';
      font-size: 13pt;

      .token {
      }
      .gloss {
        font-style: italic;
        color: $gray-600;
        font-size: 11pt;
      }
    }
  }
}
</style>

