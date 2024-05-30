<template>
  <svg class="horizontal-bar-chart" viewBox="0 0 300 100">
    <rect x="0" y="20" width="300" height="30" fill="#CCCCCC" />
    <rect x="0" y="20" height="30" :width="barWidth" :class="colorClass" />
    <text class="rate" x="150" y="10" text-anchor="middle">{{ rate | percentage }}</text>
    <text class="label" x="150" y="75" text-anchor="middle">{{ label }}</text>
  </svg>
</template>

<script>
  export default {
    name: 'horizontal-bar-chart',
    props: ['label', 'rate'],
    computed: {
      barWidth() {
        return `${this.rate * 300}`;
      },
      colorClass() {
        if (this.rate >= 0.95) return 'tier-1';
        if (this.rate >= 0.9) return 'tier-2';
        if (this.rate >= 0.8) return 'tier-3';
        if (this.rate >= 0.5) return 'tier-4';
        return 'tier-5';
      },
    },
    filters: {
      percentage: (n) => `${(n * 100).toFixed(1)}%`,
    },
  };
</script>

<style lang="scss">
  @import "../../../scss/config";
  .horizontal-bar-chart {
    width: 100%;
    height: 130px;

    .rate {
      font-size: 16pt;
    }

    .label {
      font-size: 10pt;
    }

    .tier-1 {
      fill: $tier-1-fill;
    }
    .tier-2 {
      fill: $tier-2-fill;
    }
    .tier-3 {
      fill: $tier-3-fill;
    }
    .tier-4 {
      fill: $tier-4-fill;
    }
    .tier-5 {
      fill: $tier-5-fill;
    }
  }
</style>
