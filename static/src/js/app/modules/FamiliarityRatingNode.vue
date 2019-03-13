<template>
  <span @mouseenter="onMouseEnter" @mouseleave="onMouseLeave" @click.prevent="onClick" :class="{ selected }">
    <icon name="circle" />
  </span>
</template>

<script>
  export default {
    props: ['rating', 'value'],
    computed: {
      selected() {
        return this.rating === this.value;
      }
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
      }
    }
  }
</script>
