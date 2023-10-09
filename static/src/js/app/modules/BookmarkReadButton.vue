<template>
  <button
    class="btn btn-block btn-outline-primary mb-3"
    @click.prevent="onToggleBookmark"
    :aria-pressed="isRead"
  >
    <i class="fa fa-star" aria-hidden="true"></i> {{ buttonText }}
  </button>
</template>

<script>
// CREATE A NEW CONSTANT FOR READ STATUS?
import { BOOKMARK_READ_UPDATE, BOOKMARK_FETCH } from '../constants';

export default {
  props: ['textId'],
  methods: {
    onToggleBookmark() {
      if (this.bookmark) {
        // console.log(this.bookmark.readStatus);
        this.updateBookmarkRead(this.bookmark.id, !this.bookmark.readStatus);
        // this.$store.dispatch(BOOKMARK_FETCH, this.bookmark.id);
      } else {
        return;
      }
    },
    updateBookmarkRead(bookmarkId, readStatus) {
      console.log(readStatus);
      // not updating status yet
      this.$store.dispatch(BOOKMARK_READ_UPDATE, { bookmarkId, readStatus });
      console.log(this.$store.state.bookmarks[0]);
    },
  },
  computed: {
    bookmark() {
      const textId = parseInt(this.textId, 10);
      const textFilter = (bookmark) =>
        parseInt(bookmark.text.id, 10) === textId;
      return this.$store.state.bookmarks.filter(textFilter)[0];
    },
    read() {
      if (this.$store.state.bookmarks[0]) {
        return this.$store.state.bookmarks[0].readStatus;
      }
      return true;
    },
    isRead() {
      return Boolean(this.read);
    },
    buttonText() {
      return this.isRead ? 'Mark as Unread' : 'Mark as Read';
    },
  },
  // watch property?
};
</script>
