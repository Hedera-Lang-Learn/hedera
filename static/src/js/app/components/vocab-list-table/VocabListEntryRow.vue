<template>
  <tr :class="{ 'selected-entry': selected }">
    <td @click="$emit('selectEntry', entry)">{{ entry.headword }}</td>
    <td>{{ entry.gloss }}</td>
    <td v-if="showIds">{{ entry.node }}</td>
  </tr>
</template>

<script>
  export default {
    props: ['entry', 'selected', 'showIds'],
  };
</script>

<style lang="scss" scoped>
  tr {
      border-left: 3px solid transparent;
      cursor: pointer;
  }
  tr.selected-entry {
      border-left-color: #444;
      background: #EFEFEF;
  }
</style>
