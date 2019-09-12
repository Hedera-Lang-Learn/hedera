<template>
  <span class="token">
    <span
      class="word"
      v-if="token.word"
      :class="{unresolved, selected, sameNode, 'no-lemma': noLemma, 'in-vocab-list': inVocabList, ignored }"
      @click.prevent="onClick()"
    >{{ token.word }}</span><span class="following" v-if="token.following">{{ token.following }}</span>
  </span>
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
      return this.token.inVocabList && !this.ignored;
    },
    ignored() {
      return this.token.word !== this.token.word.toLowerCase();
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
      &.ignored {
        background: $gray-300;
      }
      &.in-vocab-list {
        background: inherit;
      }
    }
  }
  .highlight-in-list {
    .ignored {
      background: $gray-300;
    }
    .in-vocab-list {
      background: hsl(120, 24%, 80%); // hedera green but lighter
    }
  }

</style>
