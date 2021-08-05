<template>
  <div class="dashboard">
    <QuickAddButton/>
  </div>
</template>
<script>
  import QuickAddButton from './components/quick-add-button';
  import { FETCH_ME } from './constants';

  export default {
    components: { QuickAddButton },
    async created() {
      await this.$store.dispatch(FETCH_ME);
    },
  };
</script>
