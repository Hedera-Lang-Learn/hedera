<template>
    <div v-if="gloss">
        <div @click.prevent="onClick">
            &bull; {{gloss.gloss}}
        </div>
    </div>
</template>
<script>

  export default {
    name: 'Gloss',
    props: ['gloss'],
    methods: {
      onClick() {
        console.log(this.gloss.pk);
        this.$emit('selected', this.gloss);
      },
    },
    computed: {
    },
  };
</script>

<style lang="scss">
@import "../../../scss/config";

</style>
