<template>
  <div class="dashboard">
    <QuickAddButton/>
    <BookmarkList/>
  </div>
</template>
<script>
  import QuickAddButton from './components/quick-add-button';
  import { PROFILE_FETCH, SUPPORTED_LANG_LIST_FETCH } from './constants';
  import BookmarkList from './modules/BookmarkList.vue';

  export default {
    components: { QuickAddButton, BookmarkList },
    async created() {
      await this.$store.dispatch(PROFILE_FETCH);
      await this.$store.dispatch(SUPPORTED_LANG_LIST_FETCH);
    },
  };
</script>
