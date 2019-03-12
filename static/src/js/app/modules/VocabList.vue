<template>
    <div class="vocab-list">
        <h4>{{ title }}</h4>
        <p>{{ description }}</p>
        <gauge-chart v-if="active" :rate="knownVocab" label="Known" />
        <button class="btn btn-block btn-outline-primary" :class="{ active }" @click.prevent="onSelect">Select</button>
        <div v-if="active" class="toggle-link-container">
          <span v-if="showInVocabList">
            The known words are highlighted.
            <a href @click.prevent="toggleKnown" v-if="active">Highlight Unknown</a>
          </span>
          <span v-else>
            The unknown words are highlighted.
            <a href @click.prevent="toggleKnown" v-if="active">Highlight Known</a>
          </span>
        </div>
    </div>
</template>

<script>
import { TOGGLE_SHOW_IN_VOCAB_LIST } from '../constants';

export default {
    props: ['vocabList'],
    computed: {
      active() {
        return this.vocabList.id === this.$store.state.selectedVocabList;
      },
      title() {
        return this.vocabList.title;
      },
      description() {
        return this.vocabList.description;
      },
      knownVocab() {
        return this.$store.getters.knownVocab;
      },
      showInVocabList() {
        return this.$store.state.showInVocabList;
      },
    },
    methods: {
      onSelect() {
        this.$emit('toggleSelected', { id: this.vocabList.id });
      },
      toggleKnown() {
        this.$store.dispatch(TOGGLE_SHOW_IN_VOCAB_LIST);
      }
    }
}
</script>

<style lang="scss">
  @import "../../../scss/config";

  .vocab-list {
    h4 {
      font-size: 14pt;
    }
    p {
      font-size: 10pt;
      color: $gray-700;
    }
    .toggle-link-container {
      margin-top: 10px;
      text-align: center;
    }
    a {
      display: block;
      text-align: center;
      margin-top: 5px;
    }
    margin-bottom: 25px;
    background: $gray-100;
    padding: 15px 25px;
    border: 1px solid $gray-300;
  }
</style>
