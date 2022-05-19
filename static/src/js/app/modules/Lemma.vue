<template>
  <div v-if="lemma">
    <div
      @click.prevent="onClickLemma"
      v-for="gloss in lemma.glosses"
      :key="gloss.pk"
    >
      {{ lemma.label }}
      <Gloss :gloss="gloss" @selected="onSelectGloss"/>
    </div>
  </div>
</template>
<script>
  import Gloss from './Gloss.vue';

  export default {
    components: { Gloss },
    name: 'Lemma',
    props: ['lemma'],
    methods: {
      onSelectGloss(gloss) {
        // update token in lemmatized text with the gloss id
        console.log('selected gloss=', gloss);
        // this.$store.dispatch(UPDATE_TOKEN, {
        //   id: this.textId,
        //   tokenIndex: this.selectedToken.tokenIndex,
        //   nodeId: node.pk,
        //   resolved: RESOLVED_MANUAL,
        // });
      },
      onClickLemma() {
        // update token in lemmatized text with the lemma id
      },
    },
    computed: {

    },
  };
</script>

<style lang="scss">
@import '../../../scss/config';
</style>
