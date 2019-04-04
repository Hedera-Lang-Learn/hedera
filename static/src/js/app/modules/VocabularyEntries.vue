<template>
  <div class="vocab-entries" v-if="vocabEntries && vocabEntries.length > 0">
    <div class="vocab-entry" v-for="(entry, index) in vocabEntries" :key="index">
        <span class="headword">{{ entry.headword }}</span>
        <span class="gloss">{{ entry.gloss }}</span>
    </div>
  </div>
</template>

<script>
export default {
  props: ['vocabEntries']
}
</script>
