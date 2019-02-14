<template>
  <div class="app-container">
    <router-view />
    <aside v-if="selectedToken">
      {{ selectedToken }} @ {{ selectedIndex }}
    </aside>
  </div>
</template>
<script>
import { FETCH_ITEMS } from './constants';

export default {
  created() {
    this.$store.dispatch(FETCH_ITEMS, { id: this.$route.params.id });
  },
  computed: {
    selectedToken() {
      return this.$store.state.selectedToken;
    },
    selectedIndex() {
      return this.$store.state.selectedIndex;
    }
  }
}
</script>
