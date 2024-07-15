<template>
  <button
    class="btn btn-block btn-outline-primary mb-3"
    @click.prevent="onToggleBookmark"
    :aria-pressed="isBookmarked"
  >
    <i class="fa fa-bookmark" aria-hidden="true"></i> {{ buttonText }}
  </button>
</template>

<script>
  import { BOOKMARK_CREATE, BOOKMARK_DELETE } from '../constants';

  export default {
    props: ['textId'],
    methods: {
      onToggleBookmark() {
        if (this.bookmark) {
          this.removeBookmark(this.bookmark.id);
        } else {
          this.addBookmark(this.textId);
        }
      },
      addBookmark(textId) {
        this.$store.dispatch(BOOKMARK_CREATE, { textId });
      },
      removeBookmark(bookmarkId) {
        this.$store.dispatch(BOOKMARK_DELETE, { bookmarkId });
      },
    },
    computed: {
      bookmark() {
        const textId = parseInt(this.textId, 10);
        const textFilter = (bookmark) => parseInt(bookmark.text.id, 10) === textId;
        return this.$store.state.bookmarks.filter(textFilter)[0];
      },
      isBookmarked() {
        return Boolean(this.bookmark);
      },
      buttonText() {
        return this.isBookmarked ? 'Remove Bookmark' : 'Add Bookmark';
      },
    },
  };
</script>
