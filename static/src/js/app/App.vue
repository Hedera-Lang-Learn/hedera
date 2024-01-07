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
    LEMMATIZED_TEXT_FETCH_TOKENS,
    VOCAB_LIST_LIST,
    LEMMATIZED_TEXT_FETCH,
    PROFILE_FETCH,
    PERSONAL_VOCAB_LIST_FETCH, BOOKMARK_LIST,
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
      this.$store.dispatch(PROFILE_FETCH);
      this.$store.dispatch(BOOKMARK_LIST);
    },
    watch: {
      textId: {
        immediate: true,
        handler() {
          this.$store.dispatch(LEMMATIZED_TEXT_FETCH, { id: this.textId })
            .then(() => {
              this.$store.dispatch(VOCAB_LIST_LIST);
            });
        },
      },
      // TODO: how to make inclusive without extraneous api calls to LEM_TEXT_FETCH_TOKENS?
      // i.e. how to select tokens on top of another selected?
      // problem: updating "one after" the click
      selectedVocabList: {
        immediate: true,
        handler() {
          if ('personal' in this.selectedVocabList) {
            this.$store.dispatch(PERSONAL_VOCAB_LIST_FETCH, { lang: this.$store.state.text.lang });
          }
          // this is also screwing up the rate percentages, applying the same rate to different lists
          // Object.keys(this.selectedVocabList).forEach((id) => {
          //   this.$store.dispatch(LEMMATIZED_TEXT_FETCH_TOKENS, { id: this.textId, vocabListId: id });
          // });
          this.$store.dispatch(LEMMATIZED_TEXT_FETCH_TOKENS, { id: this.textId, vocabListId: this.selectedVocabListId[this.selectedVocabListId.length - 1] });
        },
      },
    },
    computed: {
      selectedVocabListId() {
        return this.$store.state.selectedVocabList.map((l) => l.id);
      },
      selectedVocabList() {
        console.log(this.selectedVocabListId);
        return this.$store.state.selectedVocabList;
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
