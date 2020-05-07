<template>
  <div class="familiarity-rating">
    <div class="likert-group">
        <FamiliarityRatingNode :rating="1" :value="this.value" @selected="onSelected" @active="onActive" @inactive="onInactive" />
        <FamiliarityRatingNode :rating="2" :value="this.value" @selected="onSelected" @active="onActive" @inactive="onInactive" />
        <FamiliarityRatingNode :rating="3" :value="this.value" @selected="onSelected" @active="onActive" @inactive="onInactive" />
        <FamiliarityRatingNode :rating="4" :value="this.value" @selected="onSelected" @active="onActive" @inactive="onInactive" />
        <FamiliarityRatingNode :rating="5" :value="this.value" @selected="onSelected" @active="onActive" @inactive="onInactive" />
    </div>
    <div class="help-text" v-show="help">{{ help }}</div>
  </div>
</template>

<script>
  import FamiliarityRatingNode from './FamiliarityRatingNode.vue';
  import { RATINGS } from '../constants';

  export default {
    props: ['value'],
    components: { FamiliarityRatingNode },
    data() {
      return {
        help: '',
      };
    },
    methods: {
      onSelected(rating) {
        this.$emit('input', rating);
      },
      onActive(rating) {
        this.help = RATINGS[rating];
      },
      onInactive(rating) {
        if (this.help === RATINGS[rating]) {
          this.help = '';
        }
      },
    },
  };
</script>

<style lang="scss">
  @import "../../../scss/config";

  .familiarity-rating .help-text {
    font-size: 0.8rem;
    font-style: italic;
    color: $gray-500;
  }
</style>
