<template>
  <div class="vocab-entries" v-if="vocabEntries && vocabEntries.length > 0">
    <VocabularyEntry v-for="(entry, index) in vocabEntries" :key="index" :entry="entry" :show-entry="showEntries" />
  </div>
</template>

<script>
  import VocabularyEntry from './VocabularyEntry.vue';

  export default {
    props: ['vocabEntries', 'showEntries'],
    components: { VocabularyEntry },
    data() {
      return {
        showGloss: false,
      };
    },
  };
</script>
