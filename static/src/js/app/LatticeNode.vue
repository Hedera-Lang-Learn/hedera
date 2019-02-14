<template>
  <div class="lattice-node">
    <div class="lattice-node--heading">{{ node.pk }}. {{ node.label }}</div>
    <LatticeNode v-for="child in node.children" :key="child.pk" :node="child" />
  </div>
</template>
<script>
export default {
  props: ['node'],
  name: 'LatticeNode'
}
</script>
