<template>
  <table class="table">
    <colgroup>
        <col style="width:20%">
        <col style="width:80%">
    </colgroup>
    <tr><th>Headword</th><th>Gloss</th><th>Lemma Link</th><th></th></tr>
    <VocabListEntryRow
      v-for="(entry, index) in entries" :key="`${index}-${entry.id}`"
      :selected="selectedIndex === index"
      :entry="entry"
      @select-entry="entry => $emit('select-entry', entry)"
      @edit-entry="(entryData) => $emit('edit-entry', entryData)"
      @delete-entry="(entryData) => $emit('delete-entry', entryData)"
    />
  </table>
</template>

<script>
  import VocabListEntryRow from './VocabListEntryRow.vue';

  const prevIndex = (currentIndex, tokens) => {
    let index = (currentIndex || 0) - 1;
    if (index === -1) {
      index = tokens.length - 1;
    }
    return index;
  };

  const nextIndex = (currentIndex, tokens) => {
    let index;
    if (currentIndex === undefined || currentIndex === null) {
      index = 0;
    } else {
      index = currentIndex + 1;
    }
    if (index === tokens.length) {
      index = 0;
    }
    return index;
  };

  export default {
    props: ['entries', 'selectedIndex'],
    components: { VocabListEntryRow },
    shortcuts: {
      prevVocabEntry() {
        this.goToWord(prevIndex);
      },
      nextVocabEntry() {
        this.goToWord(nextIndex);
      },
    },
    methods: {
      goToWord(indexFunction) {
        const index = indexFunction(this.selectedIndex, this.entries);
        this.$emit('selectEntry', this.entries[index]);
      },
    },
  };
</script>

<style lang="scss" scoped>
</style>
