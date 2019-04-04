<template>
  <div class="vocab-entries" v-if="vocabEntries && vocabEntries.length > 0">
    <VocabularyEntry v-for="(entry, index) in vocabEntries" :key="index" :entry="entry" />
  </div>
</template>

<script>
import VocabularyEntry from './VocabularyEntry.vue';

export default {
  props: ['vocabEntries'],
  components: { VocabularyEntry },
  data() {
    return {
      showGloss: false,
    }
  },
}
</script>
