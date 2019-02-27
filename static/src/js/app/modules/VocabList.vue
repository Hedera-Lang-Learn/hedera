<template>
    <div class="vocab-list">
        <h4>{{ title }}</h4>
        <p class="lead">{{ description }}</p>
        <button class="btn btn-block btn-outline-primary" :class="{ active }" @click.prevent="onSelect">Select</button>
    </div>
</template>
<script>
export default {
    props: ['vocabList'],
    computed: {
      active() {
        return this.vocabList.id === this.$store.state.selectedVocabList;
      },
      title() {
        return this.vocabList.title;
      },
      description() {
        return this.vocabList.description;
      }
    },
    methods: {
      onSelect() {
        this.$emit('toggleSelected', { id: this.vocabList.id });
      }
    }
}
</script>
