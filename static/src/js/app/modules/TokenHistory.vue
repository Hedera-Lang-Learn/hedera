<template>
  <div class="token-history mt-4" v-if="history.length > 0">
    <template v-if="showHistory">
      <a href @click.prevent="onHide">Hide History</a>
      <div class="items">
        <TokenHistoryItem
          v-for="item in history"
          :key="item.id"
          :item="item"
        />
      </div>
    </template>
    <a href @click.prevent="onShow" v-else>Show History</a>
  </div>
</template>

<script>
  import TokenHistoryItem from './TokenHistoryItem.vue';

  export default {
    components: {
      TokenHistoryItem,
    },
    data() {
      return {
        showHistory: false,
      };
    },
    methods: {
      onShow() {
        this.showHistory = true;
      },
      onHide() {
        this.showHistory = false;
      },
    },
    computed: {
      history() {
        return this.$store.state.selectedTokenHistory;
      },
    },
  };
</script>

<style lang="scss" scoped>
  @import "../../../scss/config";
  .items {
    background: $gray-100;
  }
</style>
