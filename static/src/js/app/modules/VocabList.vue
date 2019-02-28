<template>
    <div class="vocab-list">
        <h4>{{ title }}</h4>
        <p>{{ description }}</p>
        <gauge-chart v-if="active" :rate="knownVocab" label="Known" />
        <button class="btn btn-block btn-outline-primary" :class="{ active }" @click.prevent="onSelect">Select</button>
        <a href @click.prevent="toggleKnown" v-if="active">Highlight {{ showInVocabList ? 'Unknown' : 'Known' }}</a>
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
    a {
      margin-top: 5px;
      display: block;
      text-align: center;
    }
    margin-bottom: 25px;
    background: $gray-100;
    padding: 15px 25px;
    border: 1px solid $gray-300;
  }
</style>
