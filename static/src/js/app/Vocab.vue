<template>
  <div class="vocab-list" v-if="loading">
    <p class="lead">Loading...</p>
  </div>
  <section v-else>
    <div class="row" v-if="showToggle">
      <div class="col-8">
        <div class="text-right mb-1"><small><a href @click.prevent="toggleShowIds = !toggleShowIds">Toggle Lemma IDs</a></small></div>
      </div>
      <div class="col-4"></div>
    </div>
    <div class="vocab-list row">
       <div class="col-8">
         <VocabListTable
          @select-entry="onSelectEntry"
          @delete-entry="onDeleteEntry"
          @edit-entry="onEditEntry"
          :entries="entries"
          :selected-index="selectedIndex"
          :showIds="showIds"
          :canEdit="canEdit"
        />
      </div>
      <div class="col-4">
          <div style="position: fixed;">
            <VocabularyLemma :lemma="selectedLemma" @selected="onSelectLemma" :showIds="showIds" />
          </div>
      </div>
    </div>
  </section>
</template>

<script>
  import api from './api';
  import VocabularyLemma from './modules/VocabularyLemma.vue';
  import VocabListTable from './components/vocab-list-table';
  import { FETCH_LEMMA, FETCH_ME } from './constants';

  export default {
    props: ['vocabId'],
    components: { VocabularyLemma, VocabListTable },
    data() {
      return {
        selectedEntry: null,
        selectedLemma: null,
        entries: [],
        canEdit: false,
        loading: false,
        toggleShowIds: false,
      };
    },
    created() {
      this.$store.dispatch(FETCH_ME);
    },
    computed: {
      showToggle() {
        return this.$store.state.me.showLemmaIds === 'toggle';
      },
      showIds() {
        const { showLemmaIds } = this.$store.state.me;
        return showLemmaIds === 'always'
          || (showLemmaIds === 'toggle' && this.toggleShowIds);
      },
      selectedIndex() {
        return this.selectedEntry ? this.entries.findIndex((e) => e.id === this.selectedEntry.id) : null;
      },
    },
    methods: {
      onSelectEntry(entry) {
        this.selectedEntry = entry;
        this.selectLemma(entry.lemma);
      },
      selectLemma(lemmaPK) {
        if (lemmaPK === null) {
          // if primary key provided is null, selected lemma should also be null
          this.selectedLemma = null;
          return;
        }
        if (this.$store.state.lemmas[lemmaPK] && this.$store.state.lemmas[lemmaPK].id) {
          // if primary key provided is in state and has id, retrieve from state
          this.selectedLemma = this.$store.state.lemmas[lemmaPK];
        } else {
          // if primary key provided is not null and not in state, fetch it
          // and assign the result to selected lemma
          this.$store.dispatch(FETCH_LEMMA, { id: lemmaPK }).then(() => {
            this.selectedLemma = this.$store.state.lemmas[lemmaPK];
          });
        }
      },
      onSelectLemma(lemma) {
        if (this.canEdit) {
          api.vocabEntryLink(this.selectedEntry.id, lemma.pk, (data) => {
            this.entries.splice(this.selectedIndex, 1, data);
            this.selectLemma(lemma.pk);
          });
        }
      },
      onDeleteEntry(entryData) {
        const { entry, cb } = entryData;
        return api.deleteVocabEntry(entry.id, () => {
          const index = this.entries.findIndex((e) => e.id === entry.id);
          this.entries.splice(index, 1);
          cb();
        });
      },
      onEditEntry(entryData) {
        const {
          entry,
          headword,
          gloss,
          cb,
        } = entryData;
        return api.vocabEntryEdit(entry.id, headword, gloss, (data) => {
          const index = this.entries.findIndex((e) => e.id === entry.id);
          this.entries.splice(index, 1, data);
          cb();
        });
      },
    },
    watch: {
      vocabId: {
        immediate: true,
        handler() {
          this.loading = true;
          api.fetchVocabEntries(this.vocabId, (data) => {
            this.entries = data.data.entries;
            this.canEdit = data.data.canEdit;
            this.loading = false;
          });
        },
      },
    },
  };
</script>

<style lang="scss" scoped>
</style>
