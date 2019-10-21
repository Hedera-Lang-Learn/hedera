<template>
  <div class="mark-resolved">
    <span class="status-label">{{ resolved }}</span>
    <a href @click.prevent="toggleResolved" v-if="canChange">
      {{ label }}
    </a>
  </div>
</template>
<script>
import {
  RESOLVED_UNRESOLVED,
  RESOLVED_MANUAL,
  RESOLVED_AUTOMATIC,
} from '../constants';

export default {
  props: ['resolved'],
  computed: {
    label() {
      let label = this.resolved;
      if (this.resolved === RESOLVED_UNRESOLVED) {
        label = 'Mark Resolved';
      } else if (this.resolved === RESOLVED_AUTOMATIC || this.resolved === RESOLVED_MANUAL) {
        label = `Mark Unresolved`;
      }
      return label;
    },
    canChange() {
      return [RESOLVED_UNRESOLVED, RESOLVED_AUTOMATIC, RESOLVED_MANUAL].indexOf(this.resolved) > -1;
    }
  },
  methods: {
    toggleResolved() {
      let resolved = this.resolved;
      if (this.resolved === RESOLVED_UNRESOLVED) {
        resolved = RESOLVED_MANUAL;
      } else if (this.resolved === RESOLVED_AUTOMATIC || this.resolved === RESOLVED_MANUAL) {
        resolved = RESOLVED_UNRESOLVED;
      }
      this.$emit('toggle', { resolved });
    }
  }
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
  }
</style>
