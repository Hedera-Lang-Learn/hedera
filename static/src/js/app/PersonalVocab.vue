<template>
  <table class="table">
    <colgroup>
        <col style="width:20%">
        <col style="width:40%">
        <col style="width:40%">
    </colgroup>
    <tr>
        <th>Headword</th>
        <th>Gloss</th>
        <th>Familiarity</th>
    </tr>
    <tr v-for="entry in personalVocabEntries" :key="entry.id">
        <td>{{ entry.headword }}</a></td>
        <td>{{ entry.gloss }}</td>
        <td nowrap>
            <FamiliarityRating :value="entry.familiarity" @input="rating => onRatingChange(rating, entry)" />
        </td>
    </tr>
  </table>
</template>

<script>
  import { FETCH_PERSONAL_VOCAB_LIST, UPDATE_VOCAB_ENTRY, CREATE_VOCAB_ENTRY } from './constants';
  import FamiliarityRating from './modules/FamiliarityRating.vue';

  export default {
    props: ['lang'],
    components: { FamiliarityRating },
    watch: {
      lang: {
        immediate: true,
        handler() {
          this.$store.dispatch(FETCH_PERSONAL_VOCAB_LIST, { lang: this.lang });
        }
      },
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
    },
    computed: {
      ranks() {
        return this.personalVocabList && this.personalVocabList.statsByText[this.$store.state.textId];
      },
      personalVocabList() {
        return this.$store.state.personalVocabList;
      },
      personalVocabEntries() {
        return this.personalVocabList && this.personalVocabList.entries && this.personalVocabList.entries;
      }
    }
  }
</script>

<style lang="scss">
</style>
