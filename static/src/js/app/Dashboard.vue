<template>
  <div class="dashboard">
    UNDER CONSTRUCTION
  </div>
</template>
<script>
  import { FETCH_ME } from './constants';

  export default {
    async created() {
      await this.$store.dispatch(FETCH_ME);
    },
  };
</script>
