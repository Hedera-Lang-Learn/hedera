<template>
  <div class="dashboard">
    UNDER CONSTRUCTION
    <QuickAddButton/>
  </div>
</template>
<script>
  import { FETCH_ME } from './constants';
  import QuickAddButton from './components/quick-add-button';

  export default {
    components: { QuickAddButton },
    async created() {
      await this.$store.dispatch(FETCH_ME);
    },
  };
</script>
