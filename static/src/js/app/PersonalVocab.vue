<template>
  <div>
    <h2 v-if="isPersonal">Personal Vocabulary List</h2>
    <h2 v-else>{{ vocabList.title }}</h2>
    <div class="d-flex justify-content-between mb-2">
      <QuickAddVocabForm class="mr-2 text-left" :current-lang-tab="lang" />
      <DownloadVocab :glosses="glosses" :with-familiarity="true" />
    </div>
    <div v-if="vocabEntries">
      <vue-good-table
        :columns="columns"
        :rows="vocabEntries"
        :pagination-options="paginationOptions"
        :search-options="searchOptions"
      >
        <template slot="table-row" slot-scope="props">
          <span
            v-if="
              props.column.field == 'lemma' &&
              editingFields.entryId == props.row.id
            "
          >
            <b-form-input
              list="lemma-list-id"
              class="form-control"
              v-model="props.row.lemma"
              v-on:keyup.enter="onEnter"
              @keyup="changeCell(props.column.field, props.row)"
            ></b-form-input>
            <datalist id="lemma-list-id">
              <option
                v-for="form in partialMatchForms"
                :key="form.pk"
                :value="form.lemma"
              >
                {{ form.glosses.map((glossObj) => glossObj.gloss).join(", ") }}
              </option>
            </datalist>
          </span>
          <span
            v-if="
              props.column.field == 'headword' &&
              editingFields.entryId == props.row.id
            "
          >
            <input
              class="form-control"
              v-model="props.row.headword"
              v-on:keyup.enter="onEnter"
              @keyup="changeCell(props.column.field, props.row)"
            />
          </span>

          <div
            class="d-flex"
            v-if="
              props.column.field == 'definition' &&
              editingFields.entryId == props.row.id
            "
          >
            <input
              class="form-control"
              v-model="props.row.definition"
              v-on:keyup.enter="onEnter"
              @keyup="changeCell(props.column.field, props.row)"
            />
          </div>
          <div v-if="props.column.field == 'edit'" class="d-flex edit-width">
            <button
              id="td-edit-button"
              class="btn btn-sm edit-entry"
              href
              @click.prevent="onEdit(props.row.id, props.row)"
              v-if="editingFields.entryId != props.row.id"
            >
              <i
                class="fa fa-fw fa-pen-fancy pen-icon-size"
                aria-hidden="true"
                title="Edit Entry"
              />
            </button>
            <div class="d-flex" v-if="editingFields.entryId == props.row.id">
              <button
                id="td-delete-button"
                type="button"
                aria-label="delete"
                @click="deleteVocab(props.row.id)"
                style="padding-top: 0"
              >
                <i class="fa fa-trash" aria-hidden="true" />
              </button>
              <button
                class="btn btn-md"
                href
                @click.prevent="onSave"
                v-if="saving === false"
              >
                <i class="fas fa-save" aria-hidden="true" title="Submit" />
              </button>
              <div
                class="spinner-border text-success ml-2"
                role="status"
                v-if="saving === true"
              >
                <span class="sr-only">Loading...</span>
              </div>
            </div>
          </div>
          <div v-if="props.column.field == 'familiarity'" class="d-flex">
            <FamiliarityRating
              :value="props.row.familiarity"
              @input="(rating) => onRatingChange(rating, props.row)"
            />
          </div>

          <div v-else-if="editingFields.entryId != props.row.id">
            {{ props.formattedRow[props.column.field] }}
          </div>
        </template>
      </vue-good-table>
    </div>
    <div v-else>Loading Data</div>
  </div>
</template>

<script>
  import { VueGoodTable } from 'vue-good-table';

  import {
    FETCH_PERSONAL_VOCAB_LIST,
    UPDATE_PERSONAL_VOCAB_ENTRY,
    FETCH_ME,
    DELETE_PERSONAL_VOCAB_ENTRY,
    FETCH_LEMMAS_BY_PARTIAL_FORM,
    FETCH_VOCAB_LIST,
    DELETE_VOCAB_ENTRY,
    SET_VOCAB_LIST_TYPE,
    UPDATE_VOCAB_ENTRY,
  } from './constants';

  import FamiliarityRating from './modules/FamiliarityRating.vue';
  import DownloadVocab from './components/DownloadVocab.vue';
  import QuickAddVocabForm from './components/quick-add-button';

  export default {
    props: ['lang', 'vocabId', 'personalVocab'],
    components: {
      FamiliarityRating,
      DownloadVocab,
      QuickAddVocabForm,
      VueGoodTable,
    },
    watch: {
      lang: {
        immediate: true,
        handler() {
          if (this.personalVocab) {
            this.$store.dispatch(FETCH_PERSONAL_VOCAB_LIST, { lang: this.lang });
            this.$store.dispatch(SET_VOCAB_LIST_TYPE, { vocabListType: 'personal' });
          } else {
            this.$store.dispatch(FETCH_VOCAB_LIST, { vocabListId: this.vocabId });
            this.$store.dispatch(SET_VOCAB_LIST_TYPE, { vocabListType: 'general' });
          }
        },
      },
      vocabId: {
        immediate: true,
        handler() {
          if (this.personalVocab) {
            this.$store.dispatch(FETCH_PERSONAL_VOCAB_LIST, { lang: this.lang });
            this.$store.dispatch(SET_VOCAB_LIST_TYPE, { vocabListType: 'personal' });
          } else {
            this.$store.dispatch(FETCH_VOCAB_LIST, { vocabListId: this.vocabId });
            this.$store.dispatch(SET_VOCAB_LIST_TYPE, { vocabListType: 'general' });
          }
        },
      },
    },
    data() {
      return {
        searchOptions: {
          enabled: true,
        },
        paginationOptions: {
          enabled: true,
          perPage: 25,
          perPageDropdown: [10, 25, 50, 100],
          dropdownAllowAll: true,
          mode: 'records',
        },
        editingIdx: null,
        saving: false,
        editingFields: {
          headword: null,
          definition: null,
          currentIndex: null,
          entryId: null,
          familiarity: null,
          lemmaId: null,
        },
        vocabListType: null,
      };
    },
    created() {
      this.$store.dispatch(FETCH_ME);
      document.addEventListener('keydown', this.onKeyDown);
    },
    beforeDestroy() {
      document.removeEventListener('keydown', this.onKeyDown);
    },
    methods: {
      makeToast(statusText, statusCode) {
        this.$bvToast.toast(statusText, {
          title: statusCode,
          autoHideDelay: 5000,
          appendToast: false,
        });
      },
      async onRatingChange(rating, entry) {
        const headword = entry.headword || '';
        if (headword === '') {
          return;
        }
        const definition = entry.definition || '';
        await this.$store.dispatch(UPDATE_PERSONAL_VOCAB_ENTRY, {
          entryId: entry.id,
          familiarity: rating,
          headword,
          definition,
          lang: this.lang,
        });
        await this.$store.dispatch(FETCH_PERSONAL_VOCAB_LIST, {
          lang: this.lang,
        });
      },
      async deleteVocab(id) {
        if (this.isPersonal) {
          await this.$store.dispatch(DELETE_PERSONAL_VOCAB_ENTRY, { id });
        } else if (this.vocabList.canEdit) {
          await this.$store.dispatch(DELETE_VOCAB_ENTRY, { id });
        } else {
          this.makeToast("You don't have permission to delete this", 403);
        }
      },
      onEdit(entryId, row) {
        const { headword, definition, lemma_id: lemmaId } = row;
        this.editingFields = {
          entryId,
          headword,
          definition,
          lang: this.lang,
          lemmaId,
        };
        if (this.isPersonal) {
          const { familiarity } = row;
          this.editingFields.familiarity = familiarity;
        }
      },
      async changeCell(field, row) {
        // TODO: remove dependency on familiarity
        const value = row[field];
        const { originalIndex: index, familiarity } = row;
        this.editingFields[field] = value;
        this.editingFields.index = index;
        this.editingFields.familiarity = familiarity;
        if (field === 'lemma' && value !== '') {
          await this.$store.dispatch(FETCH_LEMMAS_BY_PARTIAL_FORM, {
            form: value,
            lang: this.lang,
          });
          const found = this.partialMatchForms.find((el) => el.lemma === value);
          if (found) {
            this.editingFields.lemmaId = found.pk;
          }
        }
      },
      async onSave() {
        // TODO: updates work, but don't appear. Looks like state and the components are updating though?
        this.saving = true;
        const {
          entryId,
          headword,
          definition,
          familiarity,
          lemmaId,
        } = this.editingFields;
        let response = null;
        console.log(`This is personal vocab list: ${this.isPersonal}`);
        if (this.isPersonal) {
          console.log('personal vocabEntries before update:');
          console.log(this.$store.state.vocabList.entries);
          response = await this.$store.dispatch(UPDATE_PERSONAL_VOCAB_ENTRY, {
            entryId,
            familiarity,
            headword,
            definition,
            lang: this.lang,
            lemmaId,
          });
          console.log('vocabEntries after update:');
          console.log(this.$store.state.vocabList.entries);
        } else {
          console.log('non-personal vocabEntries before update:');
          console.log(this.$store.state.vocabList.entries);
          response = await this.$store.dispatch(UPDATE_VOCAB_ENTRY, {
            entryId,
            headword,
            definition,
            lemmaId,
          });
          console.log('vocabEntries after update:');
          console.log(this.$store.state.vocabList.entries);
        }
        if (response) {
          const { statusText, status } = response;
          this.makeToast(statusText, `Error - ${status}`);
        } else {
          this.makeToast(
            `Successfully Updated Vocabulary ${headword}`,
            'Success!',
          );
        }
        this.saving = false;
        this.resetEdit();
      },
      onEnter() {
        this.onSave();
      },
      resetEdit() {
        this.editingFields = {
          headword: null,
          definition: null,
          currentIndex: null,
          entryId: null,
          familiarity: null,
          lemmaId: null,
        };
        this.forms = [];
        this.editingIdx = null;
      },
      onKeyDown(event) {
        if (event.key === 'Escape') {
          this.resetEdit();
        }
      },
    },
    computed: {
      columns() {
        const theColumns = [
          { label: 'Lemma', field: 'lemma' },
          { label: 'Headword', field: 'headword' },
          { label: 'Definition', field: 'definition' },
        ];

        if (this.isPersonal) {
          // Add familiarity column for personal vocab lists only
          theColumns.push({ label: 'Familiarity', field: 'familiarity', width: '10rem' });
        }

        if (this.isPersonal || this.vocabList.canEdit) {
          // Add edit column only if user can edit this vocab list
          theColumns.push({ label: 'Edit', field: 'edit' });
        }

        return theColumns;
      },
      glosses() {
        if (!this.vocabEntries) {
          return [];
        }
        return this.vocabEntries.map((e) => ({
          ...e,
          label: e.lemma,
          headword: e.headword,
          definition:
            e.glosses && e.glosses.length ? e.glosses[0].gloss : e.definition,
        }));
      },
      ranks() {
        if (this.isPersonal) {
          return (
            this.vocabList
            && this.vocabList.statsByText[this.$store.state.textId]
          );
        }
        return null;
      },
      vocabList() {
        // Retrieve vocab list from state
        return this.$store.state.vocabList;
      },
      vocabEntries() {
        // Retrieve entries on their own, or return undefined if no list is present
        console.log('computed vocab entries run');
        console.log(this.vocabList.entries);
        return this.vocabList && this.vocabList.entries;
      },
      partialMatchForms() {
        return this.$store.state.partialMatchForms;
      },
      isPersonal() {
        // Convenience prop to quickly check if vocab list is a personal vocab list
        return this.$store.state.vocabListType === 'personal';
      },
    },
  };
</script>

<style lang="scss">
@import "../../scss/config";

// mobile view - TODO may need to update later
@media only screen and (min-device-width: 360px) and (max-device-width: 812px) and (orientation: portrait) {
  #td-no-padding-left-right {
    padding-right: 0;
    padding-left: 0;
  }

  #td-no-padding-left {
    padding-left: 0;
  }

  #td-familiarity-rating {
    padding-right: 0;
    padding-left: 0;
  }
}

// other views
@media only screen and (min-device-width: 813px) {
  #td-familiarity-rating {
    display: flex;
    flex-direction: row;
  }
}
.pen-icon-size {
  width: 40px;
  height: 38px;
}
.edit-width {
  width: 83px;
  height: 2rem;
  align-items: center;
  justify-content: center;
}
.vgt-responsive {
  overflow-x: visible;
}
</style>
