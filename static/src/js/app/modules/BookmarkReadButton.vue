<template>
  <div>
    <button
      class="btn btn-block btn-outline-primary mb-3"
      @click.prevent="onToggleBookmark"
      :aria-pressed="isRead"
    >
      <i class="fa fa-check-square" aria-hidden="true"></i> {{ readButtonText }}
    </button>
  </div>
</template>

<script>
  import { BOOKMARK_READ_UPDATE } from '../constants';

  export default {
    props: ['textId'],
    methods: {
      markAsStarted() {
        setTimeout(() => {
          if (!this.bookmark.startedReadAt && !this.bookmark.readStatus) {
            this.updateBookmarkRead(this.bookmark.id, !this.bookmark.readStatus, false);
          }
        }, 10000);
      },
      onToggleBookmark() {
        if (this.bookmark) {
          this.updateBookmarkRead(this.bookmark.id, !this.bookmark.readStatus, true);
          this.markAsStarted();
        }
      },
      updateBookmarkRead(bookmarkId, readStatus, flag) {
        this.$store.dispatch(BOOKMARK_READ_UPDATE, { bookmarkId, readStatus, flag });
      },
    },
    mounted() {
      this.markAsStarted();
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
      readButtonText() {
        return this.isRead ? 'Mark as Unread' : 'Mark as Read';
      },
    },
  };
</script>
