<template>
  <div :class="customClass ? customClass : 'lattice-node'" v-if="lemma">
    <div
      :class="customClassHeading ? customClassHeading : 'lattice-node--heading'"
      @click.prevent="onClick"
    >
      <div v-if="showIds">
        <span class="lattice-id">{{ lemma.pk }}.</span>
      </div>
      <div>
        <span class="lattice-label">{{ lemma.label }}</span>
        <span v-for="gloss in lemma.glosses" :key="gloss.pk" class="lattice-gloss">{{ gloss.gloss }}</span>
      </div>
    </div>
  </div>
</template>
<script>
  const formFilter = (node, selectedWord) => {
    if (node.forms.length > 0) {
      /* remove trailing punctuation */
      const strippedToken = selectedWord.replace(/[,.?:;·—]+$/, '');
      if (node.forms[0].form === strippedToken) {
        return true;
      }
      return false;
    }
    return true;
  };

  export default {
    name: 'LatticeNode',
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
.lattice-node--heading {
  display: flex;
}
.lattice-id {
  padding-right: 0.5em;
  font-size: 9pt;
}
.lattice-label {
  font-family: "Noto Serif";
  font-size: 13pt;
}
.lattice-gloss {
  font-family: "Noto Serif";
  font-style: italic;
  color: $gray-600;
  font-size: 11pt;
}
</style>
