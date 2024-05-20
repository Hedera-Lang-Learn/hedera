<!-- <template>
  <svg class="gauge-chart" preserveAspectRatio viewBox="0 0 300 150">
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
  const scale = (n, domainMax, rangeMax) => rangeMax * (n / domainMax);

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
      },
    },
    filters: {
      percentage: (n) => `${(n * 100).toFixed(1)}%`,
    },
  };
</script>

<style lang="scss">
  @import "../../../scss/config";
  .gauge-chart {
    width: 101%;
    height: 180px;
    margin: 20px auto;

    .rate {
      font-size: 24pt;
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
</style> -->

<template>
  <svg class="horizontal-bar-chart" preserveAspectRatio viewBox="0 0 300 100">
    <rect x="0" y="20" width="300" height="30" fill="#BBBBBB" />
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
    height: 110px;
    margin: 20px auto;

    .rate {
      font-size: 16pt;
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
