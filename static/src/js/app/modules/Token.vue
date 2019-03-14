<template>
  <span class="token"
    :class="{unresolved, selected, sameNode, 'no-lemma': noLemma, 'in-vocab-list': inVocabList }"
    @click.prevent="onClick()">{{ token.token }}</span>
</template>
<script>
export default {
  props: ['token', 'index', 'selectedIndex', 'selectedToken'],
  methods: {
    onClick() {
      this.$emit('toggleSelected', { index: this.index });
    }
  },
  computed: {
    selected() {
      return this.selectedIndex && this.selectedIndex === this.index;
    },
    sameNode() {
      return this.selectedToken && this.selectedToken.node === this.token.node;
    },
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
  .sameNode {
    border-bottom: 2px solid red;
  }
  .selected,
  .selected.sameNode {
    border-bottom: 4px solid red;
  }

  .highlight-not-in-list {
    .token {
      background: hsl(0, 44%, 80%);
      &.in-vocab-list {
        background: inherit;
      }
    }
  }
  .highlight-in-list {
    .in-vocab-list {
      background: hsl(120, 24%, 80%); // hedera green but lighter
    }
  }

</style>
