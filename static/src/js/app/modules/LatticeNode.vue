<template>
  <div class="lattice-node" v-if="node">
    <LatticeNode v-for="parent in parents" :key="parent.pk" :node="parent" @selected="n => $emit('selected', n)" />
    <div class="lattice-node--heading" @click.prevent="onClick">
      <div>
        <span class="lattice-id">{{ node.pk }}.</span>
      </div>
      <div>
        <span class="lattice-label">{{ node.label }}</span>
        <span class="lattice-gloss">{{ node.gloss }}</span>
      </div>
    </div>
    <LatticeNode v-for="child in children" :key="child.pk" :node="child" @selected="n => $emit('selected', n)" />
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
    props: ['node'],
    methods: {
      onClick() {
        this.$emit('selected', this.node);
      },
    },
    computed: {
      selectedWord() {
        return this.selectedToken && this.selectedToken.word;
      },
      parents() {
        return this.node.parents && this.node.parents.filter((node) => formFilter(node, this.selectedWord));
      },
      children() {
        return this.node.children && this.node.children.filter((node) => formFilter(node, this.selectedWord));
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
