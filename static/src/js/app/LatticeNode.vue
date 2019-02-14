<template>
  <div class="lattice-node">
    <div class="lattice-node--heading" @click.prevent="onClick">{{ node.pk }}. {{ node.label }}</div>
    <LatticeNode v-for="child in node.children" :key="child.pk" :node="child" @selected="n => $emit('selected', n)" />
  </div>
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
