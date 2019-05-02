<template>
  <div class="lattice-node" v-if="node">
    <LatticeNode v-for="parent in parents" :key="parent.pk" :node="parent" @selected="n => $emit('selected', n)" />
    <div class="lattice-node--heading" @click.prevent="onClick">
      <div>{{ node.pk }}. {{ node.label }}</div>
      <VocabularyEntries :vocab-entries="vocabEntries" :show-entries="true" />
    </div>
    <LatticeNode v-for="child in children" :key="child.pk" :node="child" @selected="n => $emit('selected', n)" />
  </div>
</template>
<script>
import VocabularyEntries from './VocabularyEntries.vue';

const formFilter = (node, selectedToken) => {
  if (node.forms.length > 0) {
    if (node.forms[0].form === selectedToken) {
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
      return this.node.parents && this.node.parents.filter(node => formFilter(node, this.selectedToken.token));
    },
    children() {
      return this.node.children && this.node.children.filter(node => formFilter(node, this.selectedToken.token));
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
  .vocab-entries {
    padding-left: 2rem;
    font-weight: 500;
    font-size: 10pt;
    .gloss {
      color: $gray-600;
    }
  }
</style>

