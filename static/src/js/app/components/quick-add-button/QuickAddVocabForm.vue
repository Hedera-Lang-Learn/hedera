<template>
  <div class="form-group">
    <form id="addvocab-form" v-on:submit.prevent>
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
            aria-label="familiarity"
          />
        </div>
      </div>
      <div class="lattice-node-container" :style="showLatticeNodeList">
        <label for="LatticeNode">Suggested Gloss</label>
        <ul class="lattice-node-list">
          <li v-for="node in latticeNode" :key="node.pk">
            <button
              class="lattice-node-button"
              aria-label="suggestion"
              @keyup.enter="onSelect"
            >
              <LatticeNode
                :node="node"
                @selected="onSelect"
                :show-ids="false"
                customClassHeading="custom-lattice-node-heading"
                customClass="custom-lattice-node"
              />
            </button>
          </li>
        </ul>
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
    FETCH_ME,
    SET_LANGUAGE_PREF,
  } from '../../constants';
  import FamiliarityRating from '../../modules/FamiliarityRating.vue';
  import LatticeNode from '../../modules/LatticeNode.vue';

  export default {
    components: { FamiliarityRating, LatticeNode },
    // on creation of the dom element fetch the list of langauages/ids the user has in their personal vocab list
    async created() {
      await this.$store.dispatch(FETCH_PERSONAL_VOCAB_LANG_LIST);
      await this.$store.dispatch(FETCH_ME);
      // set pref language
      if (this.$store.state.me && this.$store.state.me.lang) {
        const foundLangListID = this.$store.state.personalVocabLangList.find(
          (ele) => ele.lang === this.$store.state.me.lang,
        );
        this.vocabularyListId = foundLangListID.id || null;
      }
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
        submitting: false,
      };
    },
    methods: {
      onRatingChange(rating) {
        this.familiarityRating = rating;
      },
      async handleSubmit() {
        this.showUnsuccessfullAlert = false;
        this.showSuccesAlert = false;
        this.submitting = true;

        const { headword, gloss, vocabularyListId } = this;
        if (!headword || !gloss || !vocabularyListId) {
          this.submitting = false;
          return;
        }

        await this.$store.dispatch(CREATE_PERSONAL_VOCAB_ENTRY, {
          headword,
          gloss,
          vocabularyListId,
          familiarity: this.familiarityRating,
          node: this.latticeNodeId,
        });
        if (this.$store.state.personalVocabAdded) {
          this.headword = null;
          this.gloss = null;
          this.showSuccesAlert = true;
          this.$store.dispatch(RESET_LATTICE_NODES_BY_HEADWORD);
        } else {
          this.showUnsuccessfullAlert = true;
        }
        // updates pref language on form submit
        if (this.vocabularyListId) {
          const prefLang = this.$store.state.personalVocabLangList.find(
            (ele) => ele.id === this.vocabularyListId,
          );
          if (prefLang.lang !== this.$store.state.me.lang) {
            await this.$store.dispatch(SET_LANGUAGE_PREF, {
              lang: prefLang.lang,
            });
          }
        }
        this.submitting = false;
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
        this.showSuccesAlert = false;
        this.showUnsuccessfullAlert = false;
        this.$store.dispatch(RESET_LATTICE_NODES_BY_HEADWORD);
      },
      async getHeadword() {
        await this.$store.dispatch(FETCH_LATTICE_NODES_BY_HEADWORD, {
          headword: this.headword,
        });
      },
      onSelect(node) {
        const { gloss, pk } = node;
        if (pk) {
          this.gloss = gloss;
          this.latticeNodeId = pk;
        }
      },
    // pref language
    },
    computed: {
      // gives access to the state store of personalVocabLangList
      personalVocabLangList() {
        return this.$store.state.personalVocabLangList;
      },
      // filters lattice node to exclude parent data for simplier UI in LatticeNode component
      latticeNode() {
        const nodes = this.$store.state.latticeNodes;
        if (nodes.length) {
          const formatedNodes = nodes.map((node) => {
            const {
              canonical, gloss, label, lemmas, pk,
            } = node;
            return {
              canonical,
              gloss,
              label,
              lemmas,
              pk,
            };
          });
          return formatedNodes;
        }
        return null;
      },
      showLatticeNodeList() {
        if (!this.latticeNode) {
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
.custom-lattice-node-heading {
  display: flex;
  border: 1px solid transparent;
  &:hover {
    border: 1px solid #578e57;
  }
}
.custom-lattice-node {
  padding-left: none;
}
.lattice-node-button {
  background-color: white;
  color: black;
  margin-top: 10px;
}
.lattice-node-list {
  height: 200px;
  overflow: auto;
  list-style-type: none;
  padding-left: 0;
}
.lattice-node-container {
  padding-top: 10px;
  font-weight: bold;
}
</style>
