<template>
  <span class="token"
    :class="{unresolved, selected, 'no-lemma': noLemma }"
    @click.prevent="onClick()">{{ token.token }}</span>
  </span>
</template>
<script>
export default {
  props: ['token', 'index', 'selected'],
  methods: {
    onClick() {
      this.$emit('toggleSelected', { token: this.token, index: this.index });
    }
  },
  computed: {
    unresolved() {
      return !this.token.resolved;
    },
    noLemma() {
      return this.token.node === null;
    }
  }
};
</script>
