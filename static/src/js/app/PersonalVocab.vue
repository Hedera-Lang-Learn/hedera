<template>
  <div>
     <div class="d-flex justify-content-between mb-2">
       <QuickAddVocabForm class="mr-2 text-left" :current-lang-tab="lang"/>
       <DownloadVocab :glosses="glosses" :with-familiarity="true" />
     </div>
    <div v-if="personalVocabEntries">
      <vue-good-table
       :columns="columns"
       :rows="personalVocabEntries"
       :pagination-options="paginationOptions"
       :search-options="searchOptions"
      >
        <template slot="table-row" slot-scope="props">
          <div v-if="props.column.field == 'familiarity'" class="d-flex">
            <FamiliarityRating :value="props.row.familiarity" @input="(rating) => onRatingChange(rating, props.row)" />
            <button id="td-delete-button" type="button" aria-label="delete" @click="deleteVocab(props.row.id)" style="padding-top: 0;">
              <i class="fa fa-trash" aria-hidden="true"></i>
            </button>
          </div>
          <div v-else>
            {{props.formattedRow[props.column.field]}}
          </div>
        </template>
      </vue-good-table>
    </div>
  </div>
</template>

<script>
  import { VueGoodTable } from 'vue-good-table';

  import {
    FETCH_PERSONAL_VOCAB_LIST,
    UPDATE_VOCAB_ENTRY,
    FETCH_ME,
    DELETE_PERSONAL_VOCAB_ENTRY,
  } from './constants';

  import FamiliarityRating from './modules/FamiliarityRating.vue';
  import DownloadVocab from './components/DownloadVocab.vue';
  import QuickAddVocabForm from './components/quick-add-button';

  export default {
    props: ['lang'],
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
          this.$store.dispatch(FETCH_PERSONAL_VOCAB_LIST, { lang: this.lang });
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
        columns: [
          { label: 'Headword', field: 'headword' },
          { label: 'Gloss', field: 'gloss' },
          { label: 'Familiarity', field: 'familiarity' },
        ],
      };
    },
    created() {
      this.$store.dispatch(FETCH_ME);
    },
    methods: {
      onRatingChange(rating, entry) {
        const headword = entry.headword || '';

        if (headword === '') {
          return;
        }

        const gloss = entry.gloss || '';

        this.$store.dispatch(UPDATE_VOCAB_ENTRY, {
          entryId: entry.id,
          familiarity: rating,
          headword,
          gloss,
          lang: this.lang,
        });
      },
      deleteVocab(id) {
        this.$store.dispatch(DELETE_PERSONAL_VOCAB_ENTRY, { id });
      },
    },
    computed: {
      glosses() {
        if (!this.personalVocabEntries) {
          return [];
        }
        return this.personalVocabEntries.map((e) => ({
          ...e,
          label: e.headword,
        }));
      },
      ranks() {
        return (
          this.personalVocabList
          && this.personalVocabList.statsByText[this.$store.state.textId]
        );
      },
      personalVocabList() {
        return this.$store.state.personalVocabList;
      },
      personalVocabEntries() {
        return (
          this.personalVocabList
          && this.personalVocabList.entries
          && this.personalVocabList.entries
        );
      },
    },
  };
</script>

<style lang="scss">
@import "../../scss/config";
.personal-vocab .familiarity-rating {
  position: relative;
  .help-text {
    position: absolute;
    top: 30px;
    left: 0;
    color: $gray-700;
    background: #fff;
    padding: 2px 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16);
    z-index: 9999;
  }
}
// mobile view - TODO may need to update later
@media only screen and (min-device-width: 360px) and (max-device-width: 812px) and (orientation: portrait) {
  #td-delete-button {
    padding-left: 0;
  }
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
  #td-delete-button {
    padding-top: 0;
    padding-left: 6rem;
  }

  #td-familiarity-rating {
    display: flex;
    flex-direction: row;
  }
}
</style>
