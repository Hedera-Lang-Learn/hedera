<template>
    <div class="vocab-list">
        <h4>{{ title }}</h4>
        <p class="lead">{{ description }}</p>
        <button class="btn btn-block btn-primary" @click.prevent="onSelect">Select</button>
    </div>
</template>
<script>
export default {
    props: ['vocabList'],
    computed: {
      title() {
        return this.vocabList.title;
      },
      description() {
        return this.vocabList.description;
      }
    },
    methods: {
      onSelect() {
        this.$emit('selected', { id: this.vocabList.id });
      }
    }
}
</script>
