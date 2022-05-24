<template>
    <div v-if="gloss" class="lemma-gloss" :class="highlighted ? 'lemma-gloss--highlighted' : ''">
        <div @click.prevent="onClick">
            &bull; {{gloss.gloss}}
        </div>
    </div>
</template>
<script>

  export default {
    name: 'Gloss',
    props: ['gloss', 'highlighted'],
    methods: {
      onClick() {
        this.$emit('selected', this.gloss);
      },
    },
  };
</script>

<style lang="scss">
@import "../../../scss/config";

</style>
