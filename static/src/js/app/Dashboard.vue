<template>
  <div>
    <Modal ref="Modal"></Modal>
    <button type="button" class="btn btn-primary" @click="openModal">
      Quick Add Vocab
    </button>
  </div>
</template><script>

import Modal from './components/QuickAddVocabModal.vue'
export default {
  components: { Modal },
  methods: {
    openModal() {
      this.$refs.Modal.toggleModal()
    }
  }
};
</script>