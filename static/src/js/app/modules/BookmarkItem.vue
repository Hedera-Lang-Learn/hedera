<template>
    <li class="list-group-item bookmark-item d-flex justify-content-between">
      <a :href="bookmark.text.learnerUrl">{{ bookmark.text.title }}</a>
      <i>{{ createdAt | dateFormat('MMM D, YYYY') }}</i>
    </li>
</template>

<script>
  export default {
    props: ['bookmark'],
    data() {
      const createdAt = new Date(this.$props.bookmark.createdAt); // Should be ISO8601
      return { createdAt };
    },
  };
</script>
<style lang="scss">
  @import "../../../scss/config";
</style>
