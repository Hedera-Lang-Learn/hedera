<template>
  <li class="list-group-item bookmark-item d-flex justify-content-between">
    <a :href="bookmark.text.learnerUrl">{{ bookmark.text.title }}</a>
    <time class="bookmark-item-date" :datetime="dateMachineReadable">{{
      dateDisplay
    }}</time>
    <span v-if="bookmark.readStatus">{{ readText }}</span>
    <span v-else>{{ startText }}</span>
  </li>
</template>

<script>
  export default {
    props: ['bookmark'],
    data() {
      const createdAt = new Date(this.$props.bookmark.createdAt); // Should be ISO8601
      const isRead = this.$props.bookmark.readStatus ? 'Read' : 'Unread';
      const startedReadAt = this.$props.bookmark.startedReadAt ? new Date(this.$props.bookmark.startedReadAt) : null;
      const endedReadAt = this.$props.bookmark.endedReadAt ? new Date(this.$props.bookmark.endedReadAt) : null;
      return {
        createdAt, isRead, startedReadAt, endedReadAt,
      };
    },
    computed: {
      dateDisplay() {
        return this.$options.filters.dateFormat(
          this.$data.createdAt,
          'MMM D, YYYY',
        );
      },
      dateMachineReadable() {
        return this.$options.filters.dateFormat(
          this.$data.createdAt,
          'YYYY-MM-DD',
        );
      },
      readStatus() {
        return this.$data.isRead;
      },
      endTime() {
        return this.$options.filters.dateFormat(
          this.$data.endedReadAt,
          'MMM D, YYYY',
        );
      },
      startText() {
        if (this.$data.startedReadAt) {
          console.log(this.$data.startedReadAt);
          const startTime = this.$options.filters.dateFormat(
            this.$data.startedReadAt,
            'MMM D, YYYY',
          );
          return `Started ${startTime}`;
        }
        return 'Unread';
      },
      readText() {
        const endTime = this.$options.filters.dateFormat(
          this.$data.endedReadAt,
          'MMM D, YYYY',
        );
        return `Read ${endTime}`;
      },
    },
  };
</script>
<style lang="scss">
@import '../../../scss/config';
.bookmark-item-date {
  font-style: italic;
}
</style>
