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
    methods: {
      onGlossChange(gloss, isChecked) {
        const eventData = { lemma: this.lemma, gloss, active: isChecked };
        this.$emit('glossChange', eventData);
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
    background-color: #80b180;
  }
}
.lemma--active {
  background-color: #F0F0F0;
  border: 2px solid #80b180;
  border-radius: 4px;
}

</style>
