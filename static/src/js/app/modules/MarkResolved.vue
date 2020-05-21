<template>
  <div class="mark-resolved">
    <span class="status-label">{{ resolved }}</span>
    <a class="btn btn-block" :class="isResolved ? 'btn-outline-secondary' : 'btn-primary'" href @click.prevent="toggleResolved" v-if="canChange">
      {{ label }}
    </a>
    <a class="btn btn-primary btn-block" href @click.prevent="resolveAll" v-if="canApplyAll">
      Apply to All
    </a>
  </div>
</template>
<script>
  import {
    RESOLVED_UNRESOLVED,
    RESOLVED_MANUAL,
    RESOLVED_AUTOMATIC,
    UPDATE_TOKEN,
  } from '../constants';

  export default {
    computed: {
      label() {
        let label = this.resolved;
        if (this.resolved === RESOLVED_UNRESOLVED) {
          label = 'Mark Resolved';
        } else if (this.isResolved) {
          label = 'Mark Unresolved';
        }
        return label;
      },
      isResolved() {
        return this.resolved === RESOLVED_AUTOMATIC || this.resolved === RESOLVED_MANUAL;
      },
      canChange() {
        return [RESOLVED_UNRESOLVED, RESOLVED_AUTOMATIC, RESOLVED_MANUAL].indexOf(this.resolved) > -1;
      },
      resolved() {
        return this.selectedToken.resolved;
      },
      selectedToken() {
        return this.$store.state.selectedToken;
      },
      sameWords() {
        return this.$store.getters.sameWords;
      },
      unresolvedOthers() {
        return this.sameWords.filter((sw) => sw.tokenIndex !== this.selectedToken.tokenIndex && sw.resolved === RESOLVED_UNRESOLVED);
      },
      canApplyAll() {
        return this.unresolvedOthers.length > 0
          && [RESOLVED_AUTOMATIC, RESOLVED_MANUAL].indexOf(this.resolved) > -1;
      },
    },
    methods: {
      resolveTo(token) {
        let { resolved } = token;
        if (token.resolved === RESOLVED_UNRESOLVED) {
          resolved = RESOLVED_MANUAL;
        } else if (token.resolved === RESOLVED_AUTOMATIC || token.resolved === RESOLVED_MANUAL) {
          resolved = RESOLVED_UNRESOLVED;
        }
        return resolved;
      },
      updateToken(token) {
        this.$store.dispatch(UPDATE_TOKEN, {
          id: this.$store.state.textId,
          tokenIndex: token.tokenIndex,
          nodeId: token.node,
          resolved: this.resolveTo(token),
        });
      },
      toggleResolved() {
        this.updateToken(this.selectedToken);
      },
      resolveAll() {
        this.unresolvedOthers.forEach(this.updateToken);
      },
    },
  };
</script>

<style lang="scss" scoped>
  @import "../../../scss/config";

  .status-label {
    font-size: 80%;
    color: $gray-700;
    padding: 0px 6px;
    background: $gray-200;
    border: 1px solid $gray-400;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 20px;
  }
</style>
