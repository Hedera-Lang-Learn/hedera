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
import { BOOKMARK_READ_UPDATE } from '../constants';

// TODO: button disappears upon refresh...
export default {
  props: ['textId'],
  methods: {
    onToggleBookmark() {
      if (this.bookmark) {
        console.log(this.bookmark.readStatus);
        this.updateBookmarkRead(this.bookmark.id, !this.bookmark.readStatus);
      } else {
        return;
      }
    },
    updateBookmarkRead(bookmarkId, readStatus) {
      console.log(readStatus);
      // BUG IS HERE
      this.$store.dispatch(
        BOOKMARK_READ_UPDATE,
        { bookmarkId },
        { readStatus }
      );
    },
  },
  computed: {
    // FIGURE OUT STATE AND STORE
    bookmark() {
      const textId = parseInt(this.textId, 10);
      const textFilter = (bookmark) =>
        parseInt(bookmark.text.id, 10) === textId;
      return this.$store.state.bookmarks.filter(textFilter)[0];
    },
    isRead() {
      // needs to be readStatus - but undefined here
      // console.log(this.bookmark.readStatus);
      return Boolean(this.bookmark);
    },
    buttonText() {
      return this.isRead ? 'Mark as Unread' : 'Mark as Read';
    },
  },
};
</script>
