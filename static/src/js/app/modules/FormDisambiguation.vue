<template>
  <div class="form-disambiguation" v-if="selectedForm">
    <h4>{{ selectedForm.form }}</h4>
    <div v-for="lemma_object in selectedForm.lemmas" :key="lemma_object.pk">
      <Lemma
        :lemma="lemma_object"
        :active="isActive(lemma_object)"
        :activeGlosses="activeGlosses"
        @glossChange="onGlossChange"
        @lemmaChange="onLemmaChange"
      />
    </div>
  </div>
</template>
<script>
  import Lemma from './Lemma.vue';
  import { UPDATE_TOKEN, RESOLVED_MANUAL } from '../constants';

  const getGlossIds = (lemmas, lemma) => {
    const matchingLemmas = lemmas.filter((x) => x.pk === lemma.pk);
    if (matchingLemmas.length === 0) {
      return [];
    }
    const { glosses } = matchingLemmas[0];
    return glosses.map((gloss) => gloss.pk);
  };

  const addGloss = (glossIds, gloss) => glossIds.concat([gloss.pk]);

  const removeGloss = (glossIds, gloss) => glossIds.filter((glossId) => glossId !== gloss.pk);

  export default {
    name: 'FormDisambiguation',
    components: { Lemma },
    props: ['lemma', 'showIds', 'customClass', 'customClassHeading'],
    data() {
      return {};
    },
    methods: {
      onLemmaChange(lemma) {
        const { lemmas } = this.$store.state.forms[this.selectedToken.word_normalized];
        this.updateToken(lemma, getGlossIds(lemmas, lemma));
      },
      onGlossChange({ lemma, gloss, active }) {
        let glossIds = [];
        if (lemma.pk === this.selectedToken.lemma_id) {
          glossIds = this.selectedToken.gloss_ids;
        }
        if (active) {
          glossIds = addGloss(glossIds, gloss);
        } else {
          glossIds = removeGloss(glossIds, gloss);
        }
        this.updateToken(lemma, glossIds);
      },
      updateToken(lemma, glossIds = []) {
        this.$store.dispatch(UPDATE_TOKEN, {
          id: this.$store.state.textId,
          tokenIndex: this.selectedToken.tokenIndex,
          lemmaId: lemma.pk,
          glossIds,
          resolved: RESOLVED_MANUAL,
        });
      },
      isActive(lemma) {
        return lemma.pk === this.selectedToken.lemma_id;
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
        let form = (
          this.selectedToken
          && this.$store.state.forms[this.selectedToken.word]
        );
        if (!form) {
          form = this.selectedToken && this.$store.state.forms[this.selectedToken.word_normalized];
        }
        return form;
      },
      activeGlosses() {
        return this.selectedToken && this.selectedToken.gloss_ids;
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
