<template>
    <div class="text-familiarity">
        <div class="familiarity-null">{{ unranked }}%</div>
        <div class="familiarity-1">{{ one }}%</div>
        <div class="familiarity-2">{{ two }}%</div>
        <div class="familiarity-3">{{ three }}%</div>
        <div class="familiarity-4">{{ four }}%</div>
        <div class="familiarity-5">{{ five }}%</div>
    </div>
</template>

<script>
  const convert = (decimalString) => (parseFloat(decimalString) * 100).toFixed(1);

  export default {
    props: ['ranks'],
    computed: {
      unranked() {
        return convert(this.ranks.unranked);
      },
      one() {
        return convert(this.ranks.one);
      },
      two() {
        return convert(this.ranks.two);
      },
      three() {
        return convert(this.ranks.three);
      },
      four() {
        return convert(this.ranks.four);
      },
      five() {
        return convert(this.ranks.five);
      },
    },
  };
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

  .familiarity-null {
      background-color: $gray-300;
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
