<template>
  <div class="dashboard">
    <QuickAddButton />
    <BookmarkList />
  </div>
</template>
<script>
  import QuickAddButton from './components/quick-add-button';
  import {
    PROFILE_FETCH,
    SUPPORTED_LANG_LIST_FETCH,
    PERSONAL_VOCAB_LIST_FETCH,
    VOCAB_LIST_SET_TYPE,
  } from './constants';
  import BookmarkList from './modules/BookmarkList.vue';

  export default {
    components: { QuickAddButton, BookmarkList },
    async created() {
      await this.$store.dispatch(PROFILE_FETCH);
      await this.$store.dispatch(SUPPORTED_LANG_LIST_FETCH);
      // Dashboard quick add will default to personal vocab list
      let lang = this.lang || null;
      // look up lang if null
      if (!this.lang) {
        lang = (this.$store.state.me.lang
          || this.$store.state.personalVocabLangList)
          && this.$store.state.personalVocabLangList[0].lang;
      }
      this.$store.dispatch(PERSONAL_VOCAB_LIST_FETCH, { lang });
      this.$store.dispatch(VOCAB_LIST_SET_TYPE, { vocabListType: 'personal' });
    },
  };
</script>
