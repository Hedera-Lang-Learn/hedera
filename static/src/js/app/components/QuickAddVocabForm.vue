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
          v-on:input="getHeadword"
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
      <LatticeNode
        :node="latticeNode"
        @selected="onSelect"
        :show-ids="true"
        customClassHeading="custom-lattice-node-heading"
        customClass="custom-lattice-node"
      />
      <button type="submit" class="btn btn-primary mt-3" aria-label="Submit">
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
    FETCH_LATTICE_NODES_BY_HEADWORD,
    RESET_LATTICE_NODES_BY_HEADWORD,
  } from '../constants';
  import FamiliarityRating from '../modules/FamiliarityRating.vue';
  import LatticeNode from '../modules/LatticeNode.vue';

  export default {
    components: { FamiliarityRating, LatticeNode },
    // on creation of the dom element fetch the list of langauages/ids the user has in their personal vocab list
    async created() {
      await this.$store.dispatch(FETCH_PERSONAL_VOCAB_LANG_LIST);
    },
    data() {
      return {
        vocabularyListId: null,
        headword: null,
        gloss: null,
        latticeNodeId: null,
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
        this.$nextTick(() => {
          this.$refs.select.focus();
        });
      },
      // method function for parent components to reset the form when modal is closed
      resetForm() {
        this.headword = null;
        this.gloss = null;
        this.vocabularyListId = null;
        this.showSuccesAlert = false;
        this.showUnsuccessfullAlert = false;
        this.$store.dispatch(RESET_LATTICE_NODES_BY_HEADWORD);
      },
      async getHeadword() {
        await this.$store.dispatch(FETCH_LATTICE_NODES_BY_HEADWORD, {
          headword: this.headword,
        });
      },
      onSelect() {
        this.gloss = this.$store.state.latticeNodes[0].gloss;
      },
    },
    computed: {
      // gives access to the state store of personalVocabLangList
      personalVocabLangList() {
        return this.$store.state.personalVocabLangList;
      },
      // filters lattice node to exclude parent data for simplier UI in LatticeNode component
      latticeNode() {
        const node = this.$store.state.latticeNodes[0];
        if (node) {
          const {
            canonical, gloss, label, lemmas, pk,
          } = node;
          return {
            canonical, gloss, label, lemmas, pk,
          };
        }
        return null;
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
.custom-lattice-node-heading {
  display: flex;
}
.custom-lattice-node {
  padding-left: none;
}
</style>
