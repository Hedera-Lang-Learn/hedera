<template>
    <div class="input-group add-lemma">
        <input type="text" class="form-control" placeholder="Add Lemma" v-model="model.lemma" />
        <div class="input-group-append">
            <button class="btn btn-outline-secondary" type="button" @click.prevent="onClick">Add</button>
        </div>
    </div>
</template>

<script>
  export default {
    data() {
      return {
        model: {
          lemma: '',
        },
      };
    },
    methods: {
      onClick() {
        this.$emit('addLemma', { lemma: this.model.lemma });
        this.model.lemma = '';
      },
    },
  };
</script>

<style lang="scss">
  .add-lemma {
    margin-top: 0.5rem;
    margin-left: 2rem;
  }
</style>
