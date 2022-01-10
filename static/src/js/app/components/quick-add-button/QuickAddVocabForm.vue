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
          placeholder="gloss"
          aria-label="gloss"
          v-model="gloss"
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
      <div class="lattice-node-container" :style="showLatticeNodeList">
        <label for="LatticeNode">Suggested Gloss</label>
        <select
          id="lattice-node-select"
          v-model="latticeNodeId"
          @change="onSelect"
          aria-label="Suggested Gloss List"
        >
          <option
            id="lattice-node-options"
            v-for="node in latticeNode"
            :key="node.pk"
            :value="node.pk"
          >
            <div>
              <span
                class="lattice-label"
                :value="node.label"
                aria-label="headword"
                >{{ node.label.replace(/[0-9]/g, "") }} -
              </span>
              <span
                class="lattice-gloss"
                :value="node.gloss"
                aria-label="gloss"
                >{{ node.gloss }}</span
              >
            </div>
          </option>
        </select>
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
    CREATE_PERSONAL_VOCAB_ENTRY,
    FETCH_LATTICE_NODES_BY_HEADWORD,
    RESET_LATTICE_NODES_BY_HEADWORD,
    SET_LANGUAGE_PREF,
    FETCH_SUPPORTED_LANG_LIST,
    FETCH_ME,
  } from '../../constants';
  import FamiliarityRating from '../../modules/FamiliarityRating.vue';

  export default {
    components: { FamiliarityRating },
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
    // await this.$store.dispatch(FETCH_SUPPORTED_LANG_LIST);
    },
    data() {
      return {
        vocabularyListItem: null,
        headword: null,
        gloss: null,
        latticeNodeId: null,
        familiarityRating: 1,
        showSuccesAlert: false,
        showUnsuccessfullAlert: false,
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
      async handleSubmit() {
        this.showUnsuccessfullAlert = false;
        this.showSuccesAlert = false;
        this.submitting = true;

        const { headword, gloss, vocabularyListItem } = this;
        if (!headword || !gloss) {
          this.submitting = false;
          return;
        }
        if (this.latticeNodeId !== null) {
          const node = this.latticeNode.find(
            (ele) => parseInt(ele.pk, 10) === parseInt(this.latticeNodeId, 10),
          );
          if (node.gloss !== this.gloss) {
            this.latticeNodeId = null;
          }
        }

        await this.$store.dispatch(CREATE_PERSONAL_VOCAB_ENTRY, {
          headword,
          gloss,
          vocabularyListId: vocabularyListItem.id,
          familiarity: this.familiarityRating,
          node: this.latticeNodeId,
          lang: vocabularyListItem.lang,
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
        /**
         * TODO add more languages for searches
         * conditional to only get headword for Latin for now
         * */
        if (this.vocabularyListItem && this.vocabularyListItem.lang !== 'lat') return;
        await this.$store.dispatch(FETCH_LATTICE_NODES_BY_HEADWORD, {
          headword: this.headword,
        });
        // sets first latticenode as the default in select options
        if (this.latticeNode) {
          const { gloss, pk } = this.latticeNode[0];
          this.latticeNodeId = pk;
          this.gloss = gloss;
        }
      },
      onSelect(event) {
        // Radix must be provided to parseInt
        const node = this.latticeNode.find(
          (ele) => parseInt(ele.pk, 10) === parseInt(event.target.value, 10),
        );
        const { gloss, pk } = node;
        if (pk) {
          this.gloss = gloss;
          this.latticeNodeId = pk;
        }
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
      // filters lattice node to exclude parent data for simplier UI in LatticeNode component
      latticeNode() {
        /**
         * TODO add more languages
         * conditional to only get headword for Latin for now
         * */
        const { vocabularyListItem } = this;
        if (vocabularyListItem && vocabularyListItem.lang !== 'lat') return null;
        const nodes = this.$store.state.latticeNodes || [];
        if (!nodes.length) return null;
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

.lattice-node-container {
  padding-top: 10px;
  font-weight: bold;
}
</style>
