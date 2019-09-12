<template>
  <div class="vocab-list-entry">
    <h4>{{ title }}</h4>
    <p>{{ description }}</p>
    <button class="btn btn-block btn-outline-primary" :class="{ active }" @click.prevent="onSelect">{{ active ? 'Unselect' : 'Select' }}</button>
  </div>
</template>

<script>
  export default {
    props: ['vocabList'],
    methods: {
      onSelect() {
        this.$emit('selected', { id: this.vocabList.id });
      }
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
    }
  }
</script>

<style lang="scss" scoped>

</style>
