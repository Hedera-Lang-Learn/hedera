<template>
  <span class="familiarity-rating-node" @mouseenter="onMouseEnter" @mouseleave="onMouseLeave" @click.prevent="onClick" :class="[`rating-${rating}`, { selected }]">
    <icon name="circle" />
  </span>
</template>

<script>
  export default {
    props: ['rating', 'value'],
    computed: {
      selected() {
        return this.rating === this.value;
      },
    },
    methods: {
      onClick() {
        this.$emit('selected', this.rating);
      },
      onMouseEnter() {
        this.$emit('active', this.rating);
      },
      onMouseLeave() {
        this.$emit('inactive', this.rating);
      },
    },
  };
</script>

<style lang="scss">
  @import "../../../scss/config";

  .familiarity-rating-node {
    cursor: pointer;
    color: $gray-400;

    &.selected {
      border-bottom: none;
    }
  }
  .familiarity-rating-node:hover.rating-1,
  .selected.rating-1 {
    color: $rating-1;
  }
  .familiarity-rating-node:hover.rating-2,
  .selected.rating-2 {
    color: $rating-2;
  }
  .familiarity-rating-node:hover.rating-3,
  .selected.rating-3 {
    color: $rating-3;
  }
  .familiarity-rating-node:hover.rating-4,
  .selected.rating-4 {
    color: $rating-4;
  }
  .familiarity-rating-node:hover.rating-5,
  .selected.rating-5 {
    color: $rating-5;
  }
</style>
