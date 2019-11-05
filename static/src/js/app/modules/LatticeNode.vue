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
import VocabularyEntries from './VocabularyEntries.vue';

const formFilter = (node, selectedToken) => {
  if (node.forms.length > 0) {
    /* remove trailing punctuation */
    const strippedToken = selectedToken.replace(/[,\.\?:;·—]+$/, '');
    if (node.forms[0].form === strippedToken) {
      return true;
    } else {
      return false;
    }
  }
  return true;
}

export default {
  props: ['node'],
  name: 'LatticeNode',
  methods: {
    onClick() {
      this.$emit('selected', this.node);
    }
  },
  components: {
    VocabularyEntries,
  },
  computed: {
    parents() {
      return this.node.parents && this.node.parents.filter(node => formFilter(node, this.selectedToken.word));
    },
    children() {
      return this.node.children && this.node.children.filter(node => formFilter(node, this.selectedToken.word));
    },
    vocabEntries() {
      return this.node.vocabulary_entries;
    },
    selectedToken() {
      return this.$store.getters.selectedToken;
    }
  }
}
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
