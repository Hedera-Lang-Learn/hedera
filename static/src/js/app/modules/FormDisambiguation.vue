<template>
  <div class="form-disambiguation" v-if="selectedForm">
    <h4>{{ selectedForm.form }}</h4>
    <div v-for="form_lemma in selectedForm.lemmas" :key="form_lemma.pk">
      <Lemma
        :lemma="form_lemma"
        :highlighted="isLemmaHighlighted(form_lemma)"
        :highlightedGlosses="gloss_ids"
        @selected="onSelectLemmaGloss" />
    </div>
  </div>
</template>
<script>
  import Lemma from './Lemma.vue';

  // const formFilter = (node, selectedWord) => {
  //   if (node.forms.length > 0) {
  //     /* remove trailing punctuation */
  //     const strippedToken = selectedWord.replace(/[,.?:;·—]+$/, '');
  //     if (node.forms[0].form === strippedToken) {
  //       return true;
  //     }
  //     return false;
  //   }
  //   return true;
  // };

  export default {
    name: 'FormDisambiguation',
    components: { Lemma },
    props: ['lemma', 'showIds', 'customClass', 'customClassHeading'],
    data() {
      return {
        lemma_id: this.$store.state.selectedToken.lemma_id,
        gloss_ids: [this.$store.state.selectedToken.gloss_id],
      };
    },

    methods: {

      onSelectLemmaGloss({ lemma, gloss }) {
        console.log('selectedLemmaGloss', lemma, gloss);
        if (this.lemma_id !== lemma.pk) {
          this.gloss_ids = [];
        }
        this.lemma_id = lemma.pk;
        if (gloss) {
          this.gloss_ids.push(gloss.pk);
        }
        console.log('after selectedLemmaGloss', this.lemma_id, this.gloss_ids);
      },
      updateToken() {
        // this.$store.dispatch(UPDATE_TOKEN, {
        //   id: this.textId,
        //   tokenIndex: this.selectedToken.tokenIndex,
        //   nodeId: node.pk,
        //   resolved: RESOLVED_MANUAL,
        // });
      },
      isLemmaHighlighted(lemma) {
        return lemma.pk === this.lemma_id;
      },
    },
    computed: {
      selectedWord() {
        return this.selectedToken && this.selectedToken.word;
      },
      selectedLemma() {
        return (
          this.selectedToken
          && this.$store.state.lemmas[this.selectedToken.lemma_id]
        );
      },
      selectedToken() {
        return this.$store.state.selectedToken;
      },
      selectedForm() {
        return (
          this.selectedToken
          && this.$store.state.forms[this.selectedToken.word_normalized]
        );
      },
    },
  };
</script>

<style lang="scss">
@import '../../../scss/config';
.lattice-node--heading {
  display: flex;
}
.lattice-id {
  padding-right: 0.5em;
  font-size: 9pt;
}
.lattice-label {
  font-family: 'Noto Serif';
  font-size: 13pt;
}
.lattice-gloss {
  font-family: 'Noto Serif';
  font-style: italic;
  color: $gray-600;
  font-size: 11pt;
}
</style>
