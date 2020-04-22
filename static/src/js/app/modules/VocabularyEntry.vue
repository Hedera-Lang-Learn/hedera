<template>
    <div class="vocab-entry">
        <span class="headword">{{ entry.headword }}</span>
        <span class="gloss" v-if="showGloss || showEntry">{{ entry.gloss }}</span>
        <a href @click.prevent="showGloss = true" v-else>Reveal Gloss</a>
    </div>
</template>

<script>
  export default {
    props: ['entry', 'showEntry'],
    data() {
      return {
        showGloss: false,
      };
    },
    watch: {
      entry: {
        immediate: true,
        handler() {
          this.showGloss = false;
        },
      },
    },
  };
</script>
