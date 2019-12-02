<template>
  <tr :class="{ 'selected-entry': selected }">
    <td @click="$emit('selectEntry', entry)">{{ entry.headword }}</td>
    <td>{{ entry.gloss }}</td>
  </tr>
</template>

<script>
  export default {
    props: ['entry', 'selected']
  }
</script>

<style lang="scss" scoped>
  tr {
      border-left: 3px solid transparent;
  }
  tr.selected-entry {
      border-left-color: #444;
      background: #EFEFEF;
  }
</style>
