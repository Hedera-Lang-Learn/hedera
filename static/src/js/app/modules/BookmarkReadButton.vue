<template>
  <div>
    <button
      v-if="notStarted"
      class="btn btn-block btn-outline-primary mb-3"
      @click.prevent="onToggleStartRead"
    >
      <i class="fa fa-book" aria-hidden="true"></i> Mark as Started
    </button>
    <button
      v-else
      class="btn btn-block btn-outline-primary mb-3"
      @click.prevent="onToggleBookmark"
      :aria-pressed="isRead"
    >
      <i class="fa fa-check-square" aria-hidden="true"></i> {{ readButtonText }}
    </button>
  </div>
</template>

<script>
  import { BOOKMARK_READ_UPDATE, BOOKMARK_STARTED_READ_AT } from '../constants';

  export default {
    props: ['textId'],
    methods: {
      onToggleBookmark() {
        if (this.bookmark) {
          if (!this.bookmark.startedReadAt && !this.bookmark.readStatus) {
            this.updateBookmarkStartedReadAt(this.bookmark.id);
          }
          this.updateBookmarkRead(this.bookmark.id, !this.bookmark.readStatus);
        }
      },
      onToggleStartRead() {
        if (this.bookmark) {
          this.updateBookmarkStartedReadAt(this.bookmark.id);
        }
      },
      updateBookmarkRead(bookmarkId, readStatus) {
        this.$store.dispatch(BOOKMARK_READ_UPDATE, { bookmarkId, readStatus });
      },
      updateBookmarkStartedReadAt(bookmarkId) {
        this.$store.dispatch(BOOKMARK_STARTED_READ_AT, { bookmarkId });
      },
    },
    computed: {
      bookmark() {
        const textId = parseInt(this.textId, 10);
        const textFilter = (bookmark) => parseInt(bookmark.text.id, 10) === textId;
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
      notStarted() {
        if (this.bookmark) {
          if ((this.bookmark.startedReadAt === null) && this.bookmark.readStatus) {
            return false;
          }
          return (this.bookmark.startedReadAt === null);
        }
        return false;
      },
      readButtonText() {
        return this.isRead ? 'Mark as Unread' : 'Mark as Read';
      },
    },
  };
</script>
