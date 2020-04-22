<template>
  <div class="vocab-list-entry" :class="{ active }" @click.prevent="onSelect">
    <h4>{{ title }}</h4>
    <p>{{ description }}</p>
  </div>
</template>

<script>
  export default {
    props: ['vocabList'],
    methods: {
      onSelect() {
        this.$emit('selected', { id: this.vocabList.id });
      },
    },
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
    },
  };
</script>

<style lang="scss" scoped>

</style>
