<template>
  <div class="bookmark-list-wrapper">
    <h2>Bookmarked Texts</h2>
    <ul class="list-group bookmark-list" v-if="bookmarks">
      <BookmarkItem v-for="(bookmark, index) in bookmarks" :key="index" :bookmark="bookmark" />
    </ul>
    <div v-else>
      No bookmarks saved.
    </div>
  </div>
</template>

<script>
  import BookmarkItem from './BookmarkItem.vue';
  import { FETCH_BOOKMARKS } from '../constants';

  export default {
    components: { BookmarkItem },
    created() {
      this.$store.dispatch(FETCH_BOOKMARKS);
    },
    computed: {
      bookmarks() {
        return this.$store.state.bookmarks;
      },
    },
  };
</script>
<style lang="scss">
  @import "../../../scss/config";
  .bookmark-list-wrapper {
    margin-top: 1rem;
  }
</style>
