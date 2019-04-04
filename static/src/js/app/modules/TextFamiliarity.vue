<template>
    <div class="text-familiarity">
        <div class="familiarity-1">{{ ranks['1'].toFixed(1) }}%</div>
        <div class="familiarity-2">{{ ranks['2'].toFixed(1) }}%</div>
        <div class="familiarity-3">{{ ranks['3'].toFixed(1) }}%</div>
        <div class="familiarity-4">{{ ranks['4'].toFixed(1) }}%</div>
        <div class="familiarity-5">{{ ranks['5'].toFixed(1) }}%</div>
    </div>
</template>

<script>
export default {
    props: ['ranks'],
}
</script>

<style lang="scss">
  @import "../../../scss/config";

  .text-familiarity {
      margin-bottom: 20px;
      display: flex;
      justify-content: space-between;
      div {
          text-align: center;
          padding: 2px 8px;
          border-radius: 4px;
      }
  }

  .familiarity-1 {
    color: $white;
    background-color: $rating-1;
  }
  .familiarity-2 {
    background-color: $rating-2;
  }
  .familiarity-3 {
    background-color: $rating-3;
  }
  .familiarity-4 {
    background-color: $rating-4;
  }
  .familiarity-5 {
    color: $white;
    background-color: $rating-5;
  }
</style>
