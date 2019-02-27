<template>
    <div class="input-group add-lemma">
        <input type="text" class="form-control" placeholder="Add Lemma" v-model="model.lemma" />
        <div class="input-group-append">
            <button class="btn btn-outline-secondary" type="button" @click.prevent="$emit('addLemma', { lemma: model.lemma })">Add</button>
        </div>
    </div>
</template>
<script>
export default {
  data() {
    return {
      model: {
        lemma: '',
      }
    }
  }
}
</script>
