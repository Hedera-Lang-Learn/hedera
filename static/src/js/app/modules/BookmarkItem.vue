<template>
    <li class="list-group-item bookmark-item"><a :href="bookmark.text.learnerUrl">{{ bookmark.text.title }}</a></li>
</template>

<script>
  export default {
    props: ['bookmark'],
    data() {
      return {};
    },
  };
</script>
<style lang="scss">
  @import "../../../scss/config";
</style>
