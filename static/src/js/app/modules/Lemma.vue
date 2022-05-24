<template>
  <div v-if="lemma" class="lemma" :class="highlighted ? 'lemma--highlighted' : ''">
    <span @click.prevent="onClickLemma" class="lemma-label">{{ lemma.label }}</span>
    <div v-for="gloss in lemma.glosses" :key="gloss.pk">
      <Gloss
        :gloss="gloss"
        :highlighted="isGlossHighlighted(gloss)"
        @selected="onSelectGloss" />
    </div>
  </div>
</template>
<script>
  import Gloss from './Gloss.vue';

  export default {
    components: { Gloss },
    name: 'Lemma',
    props: ['lemma', 'highlighted', 'highlightedGlosses'],
    methods: {
      onSelectGloss(gloss) {
        console.log('selected gloss', gloss.pk, gloss.gloss);
        this.$emit('selected', { lemma: this.lemma, gloss });
      },
      onClickLemma() {
        console.log('clicked lemma', this.lemma.pk, this.lemma.label);
        this.$emit('selected', { lemma: this.lemma });
      },
      isGlossHighlighted(gloss) {
        return this.highlightedGlosses.includes(gloss.pk);
      },
    },
    computed: {},
  };
</script>

<style lang="scss">
@import '../../../scss/config';

</style>
