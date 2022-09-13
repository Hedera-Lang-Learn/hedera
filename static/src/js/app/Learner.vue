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
        <BookmarkTextButton :text-id="textId"></BookmarkTextButton>
        <div>
          <div class="nav nav-tabs mb-3">
            <li class="nav-item"><a href class="nav-link" :class="{active: !readMode}" @click.prevent="readMode = false">Familiarity</a></li>
            <li class="nav-item"><a href class="nav-link" :class="{active: readMode}" @click.prevent="readMode = true">Glosses</a></li>
          </div>
        </div>
        <div class="glosses" v-if="readMode">
          <div class="text-right">
            <DownloadVocab v-if="glosses" :glosses="glosses" :with-familiarity="false" />
          </div>
          <div class="glossed-token" :class="{selected: selectedToken && gloss.node === selectedToken.node }" v-for="gloss in glosses" :key="gloss.pk">
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

            <div class="mb-5">
              <a href @click.prevent="toggleFamiliarity">{{ showFamiliarity ? 'Hide' : 'Show' }} Familiarity in Text</a>
            </div>

            <div v-if="selectedNode" class="selection-controls">
              <div class="mb-3 selected-token-wrapper">
                <span class="selected-token">{{ selectedToken.word }}</span>
                <a href @click.prevent="revealGloss = !revealGloss">{{ revealGloss ? 'Hide' : 'Show' }} Gloss</a>
              </div>
              <div class="glossed-token revealable-gloss mb-3" :class="{show: revealGloss}">
                <span class="token">{{ selectedNode.label }}</span>
                <span class="gloss">{{ selectedNode.gloss }}</span>
              </div>
              <FamiliarityRating class="familiarity-rating" :value="selectedNodeRating" @input="onRatingChange" />
            </div>
            <VocabularyEntries class="at-root" :vocabEntries="vocabEntries" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  import {
    FETCH_TOKENS, FETCH_PERSONAL_VOCAB_LIST, FETCH_TEXT, CREATE_VOCAB_ENTRY, UPDATE_VOCAB_ENTRY, FETCH_ME, FETCH_BOOKMARKS,
  } from './constants';

  import LemmatizedText from './modules/LemmatizedText.vue';
  import VocabularyEntries from './modules/VocabularyEntries.vue';
  import FamiliarityRating from './modules/FamiliarityRating.vue';
  import TextFamiliarity from './modules/TextFamiliarity.vue';
  import DownloadVocab from './components/DownloadVocab.vue';
  import BookmarkTextButton from './modules/BookmarkTextButton.vue';

  export default {
    props: ['textId'],
    components: {
      FamiliarityRating,
      LemmatizedText,
      VocabularyEntries,
      TextFamiliarity,
      DownloadVocab,
      BookmarkTextButton,
    },
    created() {
      this.$store.dispatch(FETCH_ME);
      this.$store.dispatch(FETCH_BOOKMARKS);
    },
    data() {
      return {
        selectedNodeRating: null,
        showFamiliarity: false,
        readMode: false,
        revealGloss: false,
      };
    },
    watch: {
      textId: {
        immediate: true,
        handler() {
          this.$store.dispatch(FETCH_TEXT, { id: this.textId }).then(() => this.$store.dispatch(FETCH_PERSONAL_VOCAB_LIST, { lang: this.text.lang }));
        },
      },
      selectedVocabList: {
        immediate: true,
        handler() {
          this.$store.dispatch(FETCH_TOKENS, { id: this.textId, personalVocabListId: this.selectedVocabListId });
        },
      },
      selectedNode: {
        handler() {
          if (this.personalVocabEntry) {
            this.selectedNodeRating = this.personalVocabEntry.familiarity;
          } else {
            this.selectedNodeRating = null;
          }
        },
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
      onSetRating({ rating }) {
        if (this.selectedNode) {
          this.onRatingChange(rating);
        } else {
          console.info('You need to select a node to rate with keystrokes.');
        }
      },
    },
    computed: {
      text() {
        return this.$store.state.text;
      },
      uniqueNodes() {
        return [...new Set(this.tokens.map((token) => token.node))];
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
        return this.selectedNode && this.personalVocabList && this.personalVocabList.entries && this.personalVocabList.entries.filter((e) => e.node === this.selectedNode.pk)[0];
      },
      vocabEntries() {
        return this.selectedNode && this.selectedNode.vocabulary_entries;
      },
      selectedToken() {
        return this.$store.state.selectedToken;
      },
      selectedNode() {
        return this.selectedToken && this.$store.state.nodes[this.selectedToken.node];
      },
      knownEntries() {
        return this.personalVocabList.entries.filter((e) => e.familiarity > 2);
      },
      glosses() {
        return this.uniqueNodes
          .filter((node) => this.knownEntries.filter((k) => k.node === node).length === 0)
          .map((node) => this.tokens.filter((t) => t.node === node)[0] || null)
          .filter((t) => t !== null && t.gloss !== null && t.resolved !== 'unresolved');
      },
    },
  };
</script>

<style lang="scss">
@import "../../scss/config";
.read-mode-toggle {
  text-align: center;
  label {
    display: block;
  }

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

.selection-controls {
  background: $gray-100;
  border: 1px solid $gray-200;
  padding: 10px 15px;

  .selected-token {
    font-family: 'Noto Serif';
    font-size: 20px;
    border-bottom: 4px solid red;
  }
  .selected-token-wrapper {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    a {
      font-size: 80%;
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
  .sameLemma {
    border: none;
  }
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
}
  .glossed-token {
    font-family: 'Noto Serif';
    font-size: 13pt;

    &.selected {
      border-width: 0;
      background: $highlight;
      padding: 0 0.5rem;
      margin: 0 -0.5rem;
      .gloss {
        color: $gray-800;
      }
    }
    &.revealable-gloss {
      opacity: 0;
      &.show {
        opacity: 1;
      }
    }
    .token {
    }
    .gloss {
      font-style: italic;
      color: $gray-600;
      font-size: 11pt;
    }
  }

  .familiarity-rating {
    position: relative;
    .help-text {
      position: absolute;
      top: 50px;
      left: 0;
      color: $gray-700;
      background: #FFF;
      padding: 2px 8px;
      border: 1px solid #DDD;
      border-radius: 4px;
      box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16);
      z-index: 9999;
    }
  }
</style>
