<template>
  <div class="mark-resolved">
    <a href @click.prevent="toggleResolved">
      {{ label }}
    </a>
  </div>
</template>
<script>
export default {
  props: ["resolved"],
  computed: {
    label() {
      return this.resolved ? 'Mark Unresolved' : 'Mark Resolved';
    }
  },
  methods: {
    toggleResolved() {
      this.$emit('toggle', { resolved: !this.resolved });
    }
  }
};
</script>
