<template>
  <div class="vocab-list-selected-entry">
    <h4>
      {{ title }}
      <span @click="closeVocabList">
        <icon name="times" />
      </span>
    </h4>
    <p>{{ description }}</p>
    <gauge-chart :rate="knownVocab" label="Known (Unweighted)" />
    <gauge-chart :rate="weightedKnownVocab" label="Known (Weighted)" />
    <div class="toggle-link-container">
      <span v-if="showInVocabList">
        The known words are highlighted.
        <a href @click.prevent="toggleKnown">Highlight Unknown</a>
      </span>
      <span v-else>
        The unknown words are highlighted.
        <a href @click.prevent="toggleKnown">Highlight Known</a>
      </span>
    </div>
  </div>
</template>

<script>
import { TOGGLE_SHOW_IN_VOCAB_LIST, SET_VOCAB_LIST } from "../../constants";

export default {
  props: ["vocabList"],
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
    weightedKnownVocab() {
      return this.$store.getters.weightedKnownVocab;
    },
    showInVocabList() {
      return this.$store.state.showInVocabList;
    }
  },
  methods: {
    toggleKnown() {
      this.$store.dispatch(TOGGLE_SHOW_IN_VOCAB_LIST);
    },
    closeVocabList() {
      console.log("hhhh");
      this.$store.dispatch(SET_VOCAB_LIST, { id: null });
    }
  }
};
</script>

<style lang="scss" scoped>
@import "../../../../scss/config";
h4 {
  display: flex;
  justify-content: space-between;
  span {
    margin-right: -15px;
    color: $gray-400;
    cursor: pointer;
    &:hover {
      color: $gray-800;
    }
  }
}
</style>
