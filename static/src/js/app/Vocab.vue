<template>
  <table class="table">
    <colgroup>
        <col style="width:20%">
        <col style="width:80%">
    </colgroup>
    <tr><th>Headword</th><th>Gloss</th></tr>
    <tr v-for="entry in entries" :key="entry.id">
        <td>{{ entry.headword }}</a></td>
        <td>{{ entry.gloss }}</td>
    </tr>
  </table>
</template>

<script>
  import api from './api';

  export default {
    props: ['vocabId'],
    components: { },
    data() {
      return {
        entries: [],
      }
    },
    watch: {
      vocabId: {
        immediate: true,
        handler() {
          api.fetchVocabEntries(this.vocabId, data => {
            this.entries = data.data;
          });
        }
      },
    },
  }
</script>

<style lang="scss">
</style>
