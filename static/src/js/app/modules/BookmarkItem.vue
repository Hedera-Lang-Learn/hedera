<template>
    <li class="list-group-item bookmark-item d-flex justify-content-between">
      <a :href="bookmark.text.learnerUrl">{{ bookmark.text.title }}</a>
      <time class="bookmark-item-date" :datetime="dateMachineReadable">{{ dateDisplay }}</time>
    </li>
</template>

<script>
  export default {
    props: ['bookmark'],
    data() {
      const createdAt = new Date(this.$props.bookmark.createdAt); // Should be ISO8601
      return { createdAt };
    },
    computed: {
      dateDisplay() {
        return this.$options.filters.dateFormat(this.$data.createdAt, 'MMM D, YYYY');
      },
      dateMachineReadable() {
        return this.$options.filters.dateFormat(this.$data.createdAt, 'YYYY-MM-DD');
      },
    },
  };
</script>
<style lang="scss">
  @import "../../../scss/config";
  .bookmark-item-date {
    font-style: italic;
  }
</style>
