<template>
  <div class="form-disambiguation" v-if="selectedForm">
    <h4>{{ selectedForm.form }}</h4>
    <div v-for="form_lemma in selectedForm.lemmas" :key="form_lemma.pk">
      <Lemma
        :lemma="form_lemma"
        :active="isActive(form_lemma)"
        :activeGlosses="activeGlosses"
        @glossChange="onGlossChange"
        @lemmaChange="onLemmaChange"
      />
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
        gloss_ids: [...this.$store.state.selectedToken.gloss_ids],
      };
    },

    methods: {
      onLemmaChange(lemma) {
        this.updateLemma(lemma);
        console.log('onLemmaChange', JSON.stringify({ lemma_id: this.lemma_id, gloss_ids: this.gloss_ids }));
      },
      onGlossChange({ lemma, gloss, active }) {
        if (this.lemma_id !== lemma.pk) {
          this.lemma_id = lemma.pk;
          this.gloss_ids = [];
        }

        this.updateGloss(gloss, active);
        console.log('onGlossChange', JSON.stringify({ lemma_id: this.lemma_id, gloss_ids: this.gloss_ids }));
      },
      updateLemma(lemma) {
        if (this.lemma_id !== lemma.pk) {
          this.lemma_id = lemma.pk;
          const { lemmas } = this.$store.state.forms[this.selectedToken.word_normalized];
          const matchingLemmas = lemmas.filter((x) => x.pk === lemma.pk);
          const { glosses } = matchingLemmas[0];
          this.gloss_ids = glosses.map((gloss) => gloss.pk);
          console.log('selected glosses', this.gloss_ids, glosses, matchingLemmas);
        }
      },
      updateGloss(gloss, active) {
        if (active) {
          this.gloss_ids.push(gloss.pk);
        } else {
          const index = this.gloss_ids.indexOf(gloss.pk);
          if (index >= 0) {
            this.gloss_ids.splice(index, 1);
          }
        }
      },
      updateToken() {
        // this.$store.dispatch(UPDATE_TOKEN, {
        //   id: this.textId,
        //   tokenIndex: this.selectedToken.tokenIndex,
        //   nodeId: node.pk,
        //   resolved: RESOLVED_MANUAL,
        // });
      },
      isActive(lemma) {
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
      activeGlosses() {
        return this.gloss_ids;
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
