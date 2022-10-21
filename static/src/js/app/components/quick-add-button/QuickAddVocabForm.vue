<template>
  <div class="form-group">
    <form id="addvocab-form" v-on:submit.prevent>
      <label for="FormControlSelect"
        >Select Language of Your Personal Vocabulary List</label
      >
      <select
        v-model="vocabularyListItem"
        class="form-control mb-2"
        id="FormControlSelect"
        aria-label="language List"
        ref="select"
        required
        @change="resetLatticeNodeId()"
      >
        <option
          v-for="langItem in personalVocabLangList"
          :key="langItem.id"
          :value="langItem"
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
          v-on:input="getHeadword"
          required
        />
        <input
          class="form-control ml-2 mt-2"
          type="text"
          placeholder="definition"
          aria-label="definition"
          v-model="definition"
          @change="resetLatticeNodeId()"
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
            aria-label="familiarity"
          />
        </div>
      </div>
      <div class="lemma-options-container" :style="showLemmaOptionsList">
        <label for="lemma-select">Linked definition</label>
        <div
          v-for="lemma in lemmaOptions"
          :key="lemma.pk"
        >
          <input
            type="radio"
            v-model="lemmaId"
            @change="onSelect"
            :value="lemma.pk"
            :id="`lemma-option-${lemma.pk}`"
          >
          <label :for="`lemma-option-${lemma.pk}`">
            <span class="lemma-label" aria-label="headword">{{ lemma.label.replace(/[0-9]/g, "") }}</span>
             - <span class="lemma-gloss" aria-label="gloss">{{ (lemma.glosses.length) ? lemma.glosses[0].gloss : "" }}</span>
          </label>
        </div>
      </div>
      <button
        type="submit"
        :disabled="submitting"
        class="btn btn-primary mt-3"
        aria-label="Submit"
        @click="handleSubmit"
        @keyup.enter="handleSubmit"
      >
        Submit
      </button>
    </form>
    <div
      class="alert custom-alert-success"
      role="alert"
      v-show="showSuccesAlert"
    >
      Successfully added Vocabulary Word!
    </div>
    <div class="alert alert-info" role="alert" v-show="showUnsuccessfulAlert">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
  import {
    FETCH_PERSONAL_VOCAB_LANG_LIST,
    CREATE_PERSONAL_VOCAB_ENTRY,
    RESET_LATTICE_NODES_BY_HEADWORD,
    SET_LANGUAGE_PREF,
    FETCH_SUPPORTED_LANG_LIST,
    FETCH_ME,
    FETCH_LEMMAS_BY_FORM,
    FETCH_LEMMA,
  } from '../../constants';
  import FamiliarityRating from '../../modules/FamiliarityRating.vue';

  export default {
    components: { FamiliarityRating },
    props: ['currentLangTab'],
    // on creation of the dom element fetch the list of langauages/ids the user has in their personal vocab list
    async created() {
      await this.$store.dispatch(FETCH_PERSONAL_VOCAB_LANG_LIST);
      /**
      need to fetch supported languages and profile due to django templates causing vuex state to not persistant
      ex: navigation and personal vocab templates
     * */
      await this.$store.dispatch(FETCH_ME);
      await this.$store.dispatch(FETCH_SUPPORTED_LANG_LIST);
      // set pref language
      if (this.$store.state.me && this.$store.state.me.lang) {
        const foundLangListItem = this.personalVocabLangList.find(
          (ele) => ele.lang === this.$store.state.me.lang,
        );
        this.vocabularyListItem = foundLangListItem || this.personalVocabLangList[0];
      } else {
        const [langItem] = this.personalVocabLangList;
        this.vocabularyListItem = langItem;
      }
      // change language option to what the currently selected tab on PersonalVocab.vue
      if (this.currentLangTab) {
        const foundLangListItem = this.personalVocabLangList.find(
          (ele) => ele.lang === this.currentLangTab,
        );
        this.vocabularyListItem = foundLangListItem;
      }
    // await this.$store.dispatch(FETCH_SUPPORTED_LANG_LIST);
    },
    data() {
      return {
        vocabularyListItem: null,
        headword: null,
        definition: null,
        errorMessage: 'An error has occurred. The entry could not be added.',
        lemmaOptions: [],
        lemmaId: null,
        latticeNodeId: null,
        familiarityRating: 1,
        showSuccesAlert: false,
        showUnsuccessfulAlert: false,
        submitting: false,
        suppLangKey: null,
      };
    },
    methods: {
      onRatingChange(rating) {
        this.familiarityRating = rating;
      },
      resetLatticeNodeId() {
        this.latticeNodeId = null;
      },
      /*
      Handle form submission. This should add a new vocab entry and link it
      to the selected lemma.
       */
      async handleSubmit() {
        this.showUnsuccessfulAlert = false;
        this.showSuccesAlert = false;
        this.submitting = true;

        const { headword, definition, vocabularyListItem } = this;
        if (!headword || !definition) {
          this.submitting = false;
          return;
        }

        const newEntryData = {
          headword,
          definition,
          vocabularyListId: vocabularyListItem.id,
          familiarity: this.familiarityRating,
          lang: vocabularyListItem.lang,
          lemmaId: null,
        };
        if (this.lemmaId) {
          newEntryData.lemmaId = this.lemmaId;
        }
        await this.$store.dispatch(CREATE_PERSONAL_VOCAB_ENTRY, newEntryData);

        if (this.$store.state.personalVocabAdded) {
          this.headword = null;
          this.definition = null;
          this.lemmaOptions = [];
          this.lemmaId = null;
          this.showSuccesAlert = true;
          this.$store.dispatch(RESET_LATTICE_NODES_BY_HEADWORD);
        } else {
          this.showUnsuccessfulAlert = true;
        }
        // updates pref language on form submit
        if (vocabularyListItem) {
          const prefLang = this.$store.state.personalVocabLangList.find(
            (ele) => ele.lang === vocabularyListItem.lang,
          );
          if (prefLang && prefLang.lang !== this.$store.state.me.lang) {
            await this.$store.dispatch(SET_LANGUAGE_PREF, {
              lang: prefLang.lang,
            });
          }
        }
        this.submitting = false;
      },
      formatLang(lang) {
        const { supportedLanguages } = this.$store.state;
        const found = supportedLanguages.find((ele) => ele[0] === lang);
        return found[1];
      },
      setFocus() {
        this.$nextTick(() => {
          // this.$refs.select.focus();
        });
      },
      // method function for parent components to reset the form when modal is closed
      resetForm() {
        this.headword = null;
        this.definition = null;
        this.lemmaOptions = [];
        this.lemmaId = null;
        this.showSuccesAlert = false;
        this.showUnsuccessfulAlert = false;
        this.$store.dispatch(RESET_LATTICE_NODES_BY_HEADWORD);
      },
      /*
      Get the lemma options from the database by looking up the provided
      headword as a lemma form. Runs on input to the headword field.
       */
      async getHeadword() {
        // Don't do anything if headword is empty
        if (this.headword === '') {
          return null;
        }

        // Get headword from database if it isn't already in state
        if (!Object.hasOwn(this.$store.state.forms, this.headword)) {
          await this.$store.dispatch(FETCH_LEMMAS_BY_FORM, {
            form: this.headword,
            lang: this.vocabularyListItem.lang,
          });
        }

        // Get the fetched lemmas from the forms in state
        // TODO: there is a race condition happening here because state is
        // being accessed before it has been modified if you type too fast.
        try {
          this.lemmaOptions = this.$store.state.forms[this.headword].lemmas;
        } catch (error) {
          "This is fine actually? It'll keep trying to access state until it succeeds."; // eslint-disable-line
        }
        // sets first lemma option as the default in select options
        if (this.lemmaOptions.length) {
          const { glosses, pk } = this.lemmaOptions[0];
          this.lemmaId = pk;
          this.definition = glosses.length ? glosses[0].gloss : '';
        }
        return 0;
      },
      /*
      When a lemma is selected, update component variables accordingly
       */
      async onSelect(event) {
        if (!Object.hasOwn(this.$store.state.lemmas, event.target.value)) {
          await this.$store.dispatch(FETCH_LEMMA, { id: event.target.value });
        }
        const lemma = this.$store.state.lemmas[event.target.value];
        this.definition = lemma.glosses[0].gloss;
      },
    },
    computed: {
      // gives access to the state store of personalVocabLangList
      personalVocabLangList() {
        const { personalVocabLangList, supportedLanguages } = this.$store.state;
        const formattedPersonalVocabList = supportedLanguages.map((lang) => {
          const found = personalVocabLangList.find(
            (item) => item.lang === lang[0],
          );
          if (!found) {
            return {
              lang: lang[0],
              id: null,
            };
          }
          return found;
        });
        return formattedPersonalVocabList;
      },
      showLatticeNodeList() {
        if (!this.latticeNode) {
          return { display: 'none' };
        }
        return {};
      },
      /*
      If there are no lemma options to display, set the style of the container
      to display: none;
       */
      showLemmaOptionsList() {
        if (!this.lemmaOptions.length) {
          return { display: 'none' };
        }
        return {};
      },
    },
  };
</script>

<style lang="scss">
.custom-alert-success {
  color: #155724;
  background-color: #d4edda;
  border-color: #c3e6cb;
}

.lemma-options-container {
  padding-top: 10px;
  font-weight: bold;
}
</style>
