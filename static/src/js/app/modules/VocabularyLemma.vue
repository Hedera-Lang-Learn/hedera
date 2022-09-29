<template>
  <div :class="customClass ? customClass : 'vocabulary-lemma'" v-if="lemma">
    <div
      :class="customClassHeading ? customClassHeading : 'vocabulary-lemma--heading'"
      @click.prevent="onClick"
    >
      <div v-if="showIds">
        <span class="lemma-id">{{ lemma.pk }}.</span>
      </div>
      <div>
        <span class="lemma-label">{{ lemma.label }}</span>
        <span v-for="gloss in lemma.glosses" :key="gloss.pk" class="lemma-gloss">{{ gloss.gloss }}</span>
      </div>
    </div>
  </div>
</template>

<script>
  const formFilter = (lemma, selectedWord) => {
    if (lemma.forms.length > 0) {
      /* remove trailing punctuation */
      const strippedToken = selectedWord.replace(/[,.?:;·—]+$/, '');
      if (lemma.forms[0].form === strippedToken) {
        return true;
      }
      return false;
    }
    return true;
  };

  export default {
    name: 'VocabularyLemma',
    props: ['lemma', 'showIds', 'customClass', 'customClassHeading'],
    methods: {
      onClick() {
        this.$emit('selected', this.lemma);
      },
    },
    computed: {
      selectedWord() {
        return this.selectedToken && this.selectedToken.word;
      },
      parents() {
        return (
          this.node.parents
          && this.node.parents.filter((node) => formFilter(node, this.selectedWord))
        );
      },
      children() {
        return (
          this.node.children
          && this.node.children.filter((node) => formFilter(node, this.selectedWord))
        );
      },
      vocabEntries() {
        return this.node.vocabulary_entries;
      },
    },
  };
</script>

<style lang="scss">
@import "../../../scss/config";
.vocabulary-lemma--heading {
  display: flex;
}
.lemma-id {
  padding-right: 0.5em;
  font-size: 9pt;
}
.lemma-label {
  font-family: "Noto Serif";
  font-size: 13pt;
}
.lemma-gloss {
  font-family: "Noto Serif";
  font-style: italic;
  color: $gray-600;
  font-size: 11pt;
}
</style>
