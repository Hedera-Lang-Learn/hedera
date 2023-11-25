<template>
  <div class="bookmark-list-wrapper">
    <h2>My Bookmarks</h2>
    <div v-if="hasBookmarks">
      <ul class="list-group bookmark-list">
        <BookmarkItem
          v-for="(bookmark, index) in bookmarks"
          :key="index"
          :bookmark="bookmark"
        />
      </ul>
      <h5>Total Read: {{ readCount }}</h5>
    </div>
    <div v-else>You haven't bookmarked any texts yet.</div>
  </div>
</template>

<script>
import BookmarkItem from './BookmarkItem.vue';
import { BOOKMARK_LIST } from '../constants';

export default {
  components: { BookmarkItem },
  created() {
    this.$store.dispatch(BOOKMARK_LIST);
  },
  computed: {
    bookmarks() {
      return this.$store.state.bookmarks;
    },
    hasBookmarks() {
      console.log(this.bookmarks);
      return this.bookmarks.length > 0;
    },
    readCount() {
      return this.bookmarks.filter((b) => b.readStatus == true).length;
    },
  },
};
</script>
<style lang="scss">
@import '../../../scss/config';
.bookmark-list-wrapper {
  margin-top: 1rem;
}
</style>
