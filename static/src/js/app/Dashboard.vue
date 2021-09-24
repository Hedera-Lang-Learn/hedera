<template>
  <div class="dashboard">
    <QuickAddButton/>
    <BookmarkList/>
  </div>
</template>
<script>
  import QuickAddButton from './components/quick-add-button';
  import { FETCH_ME, FETCH_SUPPORTED_LANG_LIST } from './constants';
  import BookmarkList from './modules/BookmarkList.vue';

  export default {
    components: { QuickAddButton, BookmarkList },
    async created() {
      await this.$store.dispatch(FETCH_ME);
      await this.$store.dispatch(FETCH_SUPPORTED_LANG_LIST);
    },
  };
</script>
