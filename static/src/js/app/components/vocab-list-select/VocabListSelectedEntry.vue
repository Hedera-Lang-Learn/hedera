<template>
  <div class="vocab-list-selected-entry">
    <h4>{{ title }}</h4>
    <p>{{ description }}</p>
    <gauge-chart :rate="knownVocab" label="Known" />
    <div class="toggle-link-container">
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
  import { TOGGLE_SHOW_IN_VOCAB_LIST } from '../../constants';

  export default {
    props: ['vocabList'],
    computed: {
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
      toggleKnown() {
        this.$store.dispatch(TOGGLE_SHOW_IN_VOCAB_LIST);
      }
    }
  }
</script>

<style lang="scss" scoped>

</style>
