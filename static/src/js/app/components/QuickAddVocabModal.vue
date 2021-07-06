<template>
  <div>
    <div
      class="modal fade"
      :class="{ show, 'd-block': active }"
      tabindex="-1"
      role="dialog"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add Word to Personal Vocabulary List</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="toggleModal"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <div class="form-group">
              <form id="addvocab-form" @submit.prevent="handleSubmit">
                <label for="FormControlSelect"
                  >Select Langauge of Your Personal Vocabulary List</label
                >
                <select
                  v-model="vocabularyListId"
                  class="form-control mb-2"
                  id="FormControlSelect"
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
                    v-model="headword"
                  />
                  <input
                    class="form-control ml-2 mt-2"
                    type="text"
                    placeholder="gloss"
                    v-model="gloss"
                  />
                  <div class="flex-column ml-2">
                    <label class="mb-0" for="FamilitarityRating"
                      >Familiarity</label
                    >
                    <FamiliarityRating
                      id="FamilitarityRating"
                      :style="{}"
                      customClass="d-flex"
                      :value="familiarityRating"
                      @input="(rating) => onRatingChange(rating)"
                    />
                  </div>
                </div>
                <button type="submit" class="btn btn-primary mt-3">
                  Submit
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="active" class="modal-backdrop fade show"></div>
  </div>
</template><script>
import {
  FETCH_PERSONAL_VOCAB_LANG_LIST,
  LANGUAGES,
  CREATE_PERSONAL_VOCAB_ENTRY,
} from "../constants";
import FamiliarityRating from "../modules/FamiliarityRating.vue";
export default {
  components: { FamiliarityRating },
  // on creation of the dom element fetch the list of langauages/ids the user has in their personal vocab list
  async created() {
    await this.$store.dispatch(FETCH_PERSONAL_VOCAB_LANG_LIST);
  },
  data() {
    return {
      active: false,
      show: false,
      vocabularyListId: null,
      headword: null,
      gloss: null,
      familiarityRating: 1,
    };
  },
  methods: {
    onRatingChange: function (rating) {
      this.familiarityRating = rating;
    },
    handleSubmit: function () {
      console.log({
        headword: this.headword,
        gloss: this.gloss,
        vocabulary_list_id: this.vocabularyListId,
        familiarity: this.familiarityRating,
      });
      this.$store.dispatch(CREATE_PERSONAL_VOCAB_ENTRY, {
        // nodeId: this.selectedNode.pk,
        headword: this.headword,
        gloss: this.gloss,
        vocabulary_list_id: this.vocabularyListId,
        familiarity: this.familiarityRating,
      });
      // TODO make API CALL TO CREATE WORD
    },
    /**
     * when clicking on button in bootstrap
     * the modal style set to display and after that a show class add to modal
     * so to do that we will show modal-backdrop and set modal display to block
     * then after that we will add show class to the modal and we will use setTimeout
     * to add show class because we want show class to add after the modal-backdrop show and modal display change
     * to make modal animation work
     **/
    toggleModal: function () {
      const body = document.querySelector("body");
      this.active = !this.active;
      this.active
        ? body.classList.add("modal-open")
        : body.classList.remove("modal-open");
      // mainly for smooth animation as noted above
      setTimeout(() => (this.show = !this.show), 10);
    },
    formatLang: function (lang) {
      return LANGUAGES[lang];
    },
  },
  computed: {
    // gives access to the state store of personalVocabLangList
    personalVocabLangList() {
      return this.$store.state.personalVocabLangList;
    },
  },
};
</script>