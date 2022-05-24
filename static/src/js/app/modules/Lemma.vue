<template>
  <div v-if="lemma" class="lemma-label">
    {{ lemma.label }}
    <div
      @click.prevent="onClickLemma"
      v-for="gloss in lemma.glosses"
      :key="gloss.pk"
      class="lemma-gloss"
    >
      <Gloss :gloss="gloss" @selected="onSelectGloss" class="lemma-gloss" />
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
    computed: {},
  };
</script>

<style lang="scss">
@import '../../../scss/config';
.lemma-gloss {
  text-indent: 2em;
  font-family: 'Noto Serif';
  font-style: italic;
  color: $gray-600;
  font-size: 11pt;
  &:hover {
    border: 1px solid red;
  }
}

.lemma-label {
  font-family: 'Noto Serif';
  font-size: 13pt;
  &:hover {
    border: 1px solid #999;
  }
}
</style>
