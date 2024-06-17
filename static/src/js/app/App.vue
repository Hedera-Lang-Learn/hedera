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
        <div class="select--show" @click="open = !open" v-if="!open">
          <span>See Total Known Lemma Statistics</span>
        </div>
        <div v-if="open">
          <horizontal-bar-chart :rate="unweightedKnownVocabAll" label="Total Known (Unweighted)" />
          <horizontal-bar-chart :rate="weightedKnownVocabAll" label="Total Known (Weighted)" />
          <div @click="open = !open">
            <p class="select--hide">Hide Total Known Lemmas</p>
          </div>
        </div>
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
    BOOKMARK_LIST,
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
    data() {
      return {
        open: false,
      };
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
      selectedVocabList: {
        immediate: true,
        handler() {
          this.$store.dispatch(LEMMATIZED_TEXT_FETCH_TOKENS, { id: this.textId, vocabListId: this.selectedVocabListId });
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
      weightedKnownVocabAll() {
        return this.$store.getters.weightedKnownVocabAll;
      },
      unweightedKnownVocabAll() {
        return this.$store.getters.unweightedKnownVocabAll;
      },
    },
  };
</script>

<style lang="scss">
  @import '../../scss/config';

  .select--show {
    background: $gray-100;
    border: 1px solid $gray-200;
    border-radius: 3px;
    padding: 4px 8px;
    display: flex;
    justify-content: space-between;
    margin-bottom: 15px;
    cursor: pointer;

    :hover {
      color: #208337;
    }

    >* {
      margin-top: auto;
      margin-bottom: auto;
    }

    &.open {
      // background: $white;
      border-bottom: none;
    }
  }

  .select--hide:hover {
    color: #208337;
  }

</style>
