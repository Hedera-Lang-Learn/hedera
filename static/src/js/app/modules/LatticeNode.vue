<template>
  <div class="lattice-node" v-if="node">
    <LatticeNode v-for="parent in node.parents" :key="parent.pk" :node="parent" @selected="n => $emit('selected', n)" />
    <div class="lattice-node--heading" @click.prevent="onClick">{{ node.pk }}. {{ node.label }}</div>
    <LatticeNode v-for="child in node.children" :key="child.pk" :node="child" @selected="n => $emit('selected', n)" />
  </div>
  <div class="lattice-node" v-else>No Lemma</div>
</template>
<script>
export default {
  props: ['node'],
  name: 'LatticeNode',
  methods: {
    onClick() {
      this.$emit('selected', this.node);
    }
  }
}
</script>
