<template>
  <span class="token"
    :class="{unresolved, selected, 'no-lemma': noLemma, 'in-vocab-list': inVocabList }"
    @click.prevent="onClick()">{{ token.token }}</span>
  </span>
</template>
<script>
export default {
  props: ['token', 'index', 'selected'],
  methods: {
    onClick() {
      this.$emit('toggleSelected', { index: this.index });
    }
  },
  computed: {
    inVocabList() {
      return this.token.inVocabList;
    },
    unresolved() {
      return !this.token.resolved;
    },
    noLemma() {
      return this.token.node === null;
    }
  }
};
</script>
<style lang="scss">
  @import "../../../scss/config";
  .selected {
    border-bottom: 4px solid red;
  }

  .highlight-not-in-list {
    .token {
      background: $highlight-color;
      &.in-vocab-list {
        background: inherit;
      }
    }
  }
  .highlight-in-list {
    .in-vocab-list {
      background: $highlight-color;
    }
  }

</style>
