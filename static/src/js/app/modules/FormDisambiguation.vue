<template>
  <div v-if="selectedForm">
    <div v-for="form_lemma in selectedForm.lemmas" :key="form_lemma.pk">
      <Lemma :lemma="form_lemma" @selected="onSelect" />
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
    name: 'LatticeNode',
    components: { Lemma },
    props: ['lemma', 'showIds', 'customClass', 'customClassHeading'],
    methods: {
      onSelect(gloss) {
        console.log('disabmg', gloss);
      // this.$store.dispatch(UPDATE_TOKEN, {
      //   id: this.textId,
      //   tokenIndex: this.selectedToken.tokenIndex,
      //   nodeId: node.pk,
      //   resolved: RESOLVED_MANUAL,
      // });
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
