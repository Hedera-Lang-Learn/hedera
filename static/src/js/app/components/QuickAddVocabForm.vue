<template>
  <div class="form-group">
    <form id="addvocab-form" @submit.prevent="handleSubmit">
      <label for="FormControlSelect"
        >Select Langauge of Your Personal Vocabulary List</label
      >
      <select
        v-model="vocabularyListId"
        class="form-control mb-2"
        id="FormControlSelect"
        aria-label="language List"
        ref="select"
        required
      >
        <option
          v-for="langItem in personalVocabLangList"
          :key="langItem.id"
          :value="langItem.id"
        >
          {{ formatLang(langItem.lang) }}
        </option>
      </select>
      <div class="d-flex">
        <input
          class="form-control mt-2"
          type="text"
          placeholder="headword"
          aria-label="headword"
          v-model="headword"
          required
        />
        <input
          class="form-control ml-2 mt-2"
          type="text"
          placeholder="gloss"
          aria-label="gloss"
          v-model="gloss"
          required
        />
        <div class="flex-column ml-2">
          <label class="mb-0" for="FamiliarityRating">Familiarity</label>
          <FamiliarityRating
            id="FamiliarityRating"
            :style="{}"
            customClass="d-flex"
            :value="familiarityRating"
            @input="(rating) => onRatingChange(rating)"
            aria-label="familiarityRating"
          />
        </div>
      </div>
      <button type="submit" class="btn btn-primary mt-3" aria-label="Submit" >Submit</button>
    </form>
    <div
      class="alert custom-alert-success"
      role="alert"
      v-show="showSuccesAlert"
    >
      Successfully added Vocabulary Word!
    </div>
    <div class="alert alert-info" role="alert" v-show="showUnsuccessfullAlert">
     Word was previously added
    </div>
  </div>
</template>

<script>
  import {
    FETCH_PERSONAL_VOCAB_LANG_LIST,
    LANGUAGES,
    CREATE_PERSONAL_VOCAB_ENTRY,
  } from '../constants';
  import FamiliarityRating from '../modules/FamiliarityRating.vue';

  export default {
    components: { FamiliarityRating },
    // on creation of the dom element fetch the list of langauages/ids the user has in their personal vocab list
    async created() {
      await this.$store.dispatch(FETCH_PERSONAL_VOCAB_LANG_LIST);
    },
    data() {
      return {
        vocabularyListId: null,
        headword: null,
        gloss: null,
        familiarityRating: 1,
        showSuccesAlert: false,
        showUnsuccessfullAlert: false,
      };
    },
    methods: {
      onRatingChange(rating) {
        this.familiarityRating = rating;
      },
      async handleSubmit() {
        this.showUnsuccessfullAlert = false;
        this.showSuccesAlert = false;

        await this.$store.dispatch(CREATE_PERSONAL_VOCAB_ENTRY, {
          headword: this.headword,
          gloss: this.gloss,
          vocabularyListId: this.vocabularyListId,
          familiarity: this.familiarityRating,
        });
        if (this.$store.state.personalVocabAdded) {
          this.headword = null;
          this.gloss = null;
          this.vocabularyListId = null;
          this.showSuccesAlert = true;
        } else {
          this.showUnsuccessfullAlert = true;
        }
      },
      formatLang(lang) {
        return LANGUAGES[lang];
      },
      setFocus() {
        this.$nextTick(() => { this.$refs.select.focus(); });
      },
      resetForm() {
        this.headword = null;
        this.gloss = null;
        this.vocabularyListId = null;
        this.showSuccesAlert = false;
        this.showUnsuccessfullAlert = false;
      },
    },
    computed: {
      // gives access to the state store of personalVocabLangList
      personalVocabLangList() {
        return this.$store.state.personalVocabLangList;
      },
    // TODO add suggested node functionality
    // latticeNodes(){
    //   return this.$store.state.latticeNodes[0]
    // }
    },
  };
</script>

<style lang="scss">
.custom-alert-success {
    color: #155724;
    background-color: #d4edda;
    border-color: #c3e6cb;
}
</style>
