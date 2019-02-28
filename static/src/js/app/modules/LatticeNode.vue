<template>
  <div class="lattice-node" v-if="node">
    <LatticeNode v-for="parent in parents" :key="parent.pk" :node="parent" @selected="n => $emit('selected', n)" />
    <div class="lattice-node--heading" @click.prevent="onClick">{{ node.pk }}. {{ node.label }}</div>
    <LatticeNode v-for="child in children" :key="child.pk" :node="child" @selected="n => $emit('selected', n)" />
  </div>
</template>
<script>

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
  computed: {
    parents() {
      return this.node.parents && this.node.parents.filter(node => formFilter(node, this.selectedToken.token));
    },
    children() {
      return this.node.children && this.node.children.filter(node => formFilter(node, this.selectedToken.token));
    },
    selectedToken() {
      return this.$store.state.selectedToken;
    }
  }
}
</script>
