<template>
  <div class="lemmatized-texts">
    <table class="table">
      <tr><th>Text</th><th>Language</th><th>Length</th><th>Familiarity</th><th /></tr>
      <TextRow
        v-for="text in texts"
        :key="text.id"
        :text="text"
      />
    </table>
  </div>
</template>

<script>
  import api from './api';

  import TextRow from './components/TextRow.vue';

  export default {
    components: {
      TextRow,
    },
    data() {
      return {
        texts: [],
      };
    },
    created() {
      api.fetchTexts((data) => {
        this.texts = data.data.map((datum) => ({
          ...datum.text,
          stats: datum.stats,
        }));
      });
    },
  };
</script>

<style lang="scss" scoped>

</style>
