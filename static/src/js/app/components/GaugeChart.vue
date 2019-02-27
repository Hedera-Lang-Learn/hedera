<template>
  <svg class="gauge-chart">
    <defs>
      <mask id="donut">
        <path d="M 0 150
            A 45 45, 0, 0, 1, 300 150
            L 230 150
            A 45 45, 0, 0, 0, 70, 150
            L 0 150" fill="white" stroke="black" />
      </mask>
    </defs>

    <path d="M 0 150
           A 45 45, 0, 0, 1, 300 150
           L 230 150
           A 45 45, 0, 0, 0, 70, 150
           L 0 150" fill="white" stroke="#BBBBBB" />

    <g mask="url(#donut)">
      <rect x="0" y="150"
            height="150" width="300"
            :class="colorClass"
            :transform="`rotate(${rotation} 150 150)`" />
    </g>

    <text class="rate" x="150" y="135" text-anchor="middle">{{ rate | percentage }}</text>
    <text class="label" x="150" y="180" text-anchor="middle">{{ label }}</text>
  </svg>
</template>
<script>
const scale = (n, domainMax, rangeMax) => {
  return rangeMax * ( n / domainMax );
}

export default {
  name: 'gauge-chart',
  props: ['label', 'rate'],
  computed: {
    rotation() {
      return scale(this.rate, 1, 180);
    },
    colorClass() {
      if (this.rate >= 0.95) return 'tier-1';
      if (this.rate >= 0.9) return 'tier-2';
      if (this.rate >= 0.8) return 'tier-3';
      if (this.rate >= 0.5) return 'tier-4';
      return 'tier-5';
    }
  },
  filters: {
    percentage: n => `${(n * 100).toFixed(1)}%`,
  }
}
</script>

<style lang="scss">
  @import "../../../scss/config";
  .gauge-chart {
    width: 300px;
    height: 180px;
    margin: 20px auto;

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
