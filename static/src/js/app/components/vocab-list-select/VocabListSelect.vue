<template>
  <div class="vocab-list-select" >
    <div class="vocab-list-select-dropdown" :class="{ open }">
      <div class="vocab-list-select--title" :class="{ open }" @click="open = !open">
        <span>Select a Vocab List</span>
        <icon name="caret-down" />
      </div>
      <div class="vocab-list-select--opened" v-if="open">
        <VocabListEntry v-for="vocabList in vocabLists" :key="vocabList.id" :vocab-list="vocabList" @selected="onSelect" />
      </div>
    </div>

    <VocabListSelectedEntry v-if="selectedVocabList" :vocab-list="selectedVocabList" />
  </div>
</template>

<script>
  import { SET_VOCAB_LIST } from '../../constants';
  import VocabListEntry from './VocabListEntry.vue';
  import VocabListSelectedEntry from './VocabListSelectedEntry.vue';

  export default {
    components: {
      VocabListEntry,
      VocabListSelectedEntry,
    },
    props: ['vocabLists'],
    data() {
      return {
        open: false
      }
    },
    methods: {
      onSelect(id) {
        this.$store.dispatch(SET_VOCAB_LIST, id).then(() => (this.open = false));
      }
    },
    computed: {
      selectedVocabList() {
        return this.$store.state.vocabLists.reduce((map, l) => {
          map[l.id] = l;
          return map;
        }, {})[this.$store.state.selectedVocabList];
      }
    }
  }
</script>

<style lang="scss">
  @import "../../../../scss/config";

  .vocab-list-select-dropdown.open {
      border: 1px solid $primary;
  }
  .vocab-list-select--title {
    background: $gray-100;
    border: 1px solid $gray-200;
    border-radius: 3px;
    padding: 4px 8px;
    display: flex;
    justify-content: space-between;
    cursor: pointer;
    > * {
      margin-top: auto;
      margin-bottom: auto;
    }
    &.open {
      // background: $white;
      border-bottom: none;
    }
  }
  .vocab-list-entry {
    cursor: pointer;
    background: $gray-100;
    padding: 15px 25px;
    border: 1px solid $gray-300;
    color: $gray-600;
    &.active {
      border-left: 5px solid $primary;
      color: $gray-800;
      background: $white;
    }
  }
  .vocab-list-selected-entry {
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
    margin-top: 25px;
    background: $gray-100;
    padding: 15px 25px;
    border: 1px solid $gray-300;
  }
</style>
