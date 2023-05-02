<template>
  <div v-if="lemma" class="lemma" :class="active ? 'lemma--active' : ''">
    <div @click.prevent="onClickLemma" class="lemma-label">
      {{ lemma.label }}
    </div>
    <div v-for="gloss in lemma.glosses" :key="gloss.pk">
      <Gloss
        :gloss="gloss"
        :active="isGlossActive(gloss)"
        @change="onGlossChange" />
    </div>
  </div>
</template>
<script>
  import Gloss from './Gloss.vue';

  export default {
    components: { Gloss },
    name: 'Lemma',
    props: ['lemma', 'active', 'activeGlosses'],
    data() {
      return {};
    },
    methods: {
      onGlossChange(gloss, isChecked) {
        this.$emit('glossChange', { lemma: this.lemma, gloss, active: isChecked });
      },
      onClickLemma() {
        this.$emit('lemmaChange', this.lemma);
      },
      isGlossActive(gloss) {
        return this.activeGlosses.includes(gloss.pk);
      },
    },
    computed: {},
  };
</script>

<style lang="scss">
@import '../../../scss/config';

.lemma {
  margin-left: 0;
}
.lemma-label {
  cursor: pointer;
  font-size: 16pt;
  padding: 4px;
  &:hover {
    background-color: $hedera-green;
  }
}
.lemma--active {
  background-color: #F0F0F0;
  border: 2px solid $hedera-green;
  border-radius: 4px;
}

</style>
