<template>
  <div class="app-container">
    <div class="row">
      <div class="col-8">
        <LemmatizedText />
      </div>
      <div class="col-4">
        <BookmarkTextButton :text-id="textId" />
        <a class="btn btn-block btn-outline-info mb-3" :href="this.$store.state.text.editUrl">
          <i class="fa fa-edit" aria-hidden="true"></i> Edit Text
        </a>
        <VocabListSelect class="mb-5" :vocab-lists="vocabLists" :selectedVocabList="selectedVocabList" />
        <FormDisambiguation v-if="selectedToken" />
      </div>
    </div>
  </div>
</template>
<script>
  import {
    FETCH_TOKENS,
    FETCH_VOCAB_LISTS,
    FETCH_TEXT,
    FETCH_ME,
    FETCH_PERSONAL_VOCAB_LIST, FETCH_BOOKMARKS,
  } from './constants';

  import LemmatizedText from './modules/LemmatizedText.vue';
  import VocabListSelect from './components/vocab-list-select';
  import BookmarkTextButton from './modules/BookmarkTextButton.vue';
  import FormDisambiguation from './modules/FormDisambiguation.vue';

  export default {
    props: ['textId'],
    components: {
      FormDisambiguation,
      LemmatizedText,
      VocabListSelect,
      BookmarkTextButton,
    },
    created() {
      this.$store.dispatch(FETCH_ME);
      this.$store.dispatch(FETCH_BOOKMARKS);
    },
    watch: {
      textId: {
        immediate: true,
        handler() {
          this.$store.dispatch(FETCH_TEXT, { id: this.textId })
            .then(() => {
              this.$store.dispatch(FETCH_VOCAB_LISTS);
            });
        },
      },
      selectedVocabList: {
        immediate: true,
        handler() {
          if (this.selectedVocabListId === 'personal') {
            this.$store.dispatch(FETCH_PERSONAL_VOCAB_LIST, { lang: this.$store.state.text.lang });
          }
          this.$store.dispatch(FETCH_TOKENS, { id: this.textId, vocabListId: this.selectedVocabListId });
        },
      },
    },
    computed: {
      selectedVocabListId() {
        return this.$store.state.selectedVocabList;
      },
      selectedVocabList() {
        return this.vocabLists.reduce((map, l) => {
          map[l.id] = l;
          return map;
        }, {})[this.selectedVocabListId];
      },
      vocabLists() {
        return [
          ...this.$store.state.vocabLists,
          {
            id: 'personal',
            title: 'Personal',
            description: 'Your personal vocabulary list.',
            owner: this.$store.state.me.email,
          },
        ];
      },
      selectedToken() {
        return this.$store.state.selectedToken;
      },
    },
  };
</script>
