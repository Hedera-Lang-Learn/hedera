<template>
  <button
    class="btn btn-block btn-outline-primary mb-3"
    @click.prevent="onToggleBookmark"
    :aria-pressed="isRead"
  >
    <i class="fa fa-book" aria-hidden="true"></i> {{ buttonText }}
  </button>
</template>

<script>
import { BOOKMARK_READ_UPDATE } from '../constants';

export default {
  props: ['textId'],
  methods: {
    onToggleBookmark() {
      if (this.bookmark) {
        this.updateBookmarkRead(this.bookmark.id, !this.bookmark.readStatus);
      } else {
        return;
      }
    },
    updateBookmarkRead(bookmarkId, readStatus) {
      this.$store.dispatch(BOOKMARK_READ_UPDATE, { bookmarkId, readStatus });
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
      if (this.bookmark) {
        return this.bookmark.readStatus;
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
};
</script>
