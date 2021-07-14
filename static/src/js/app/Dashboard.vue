<template>
  <div class="dashboard">
    <Modal
      ref="Modal"
      title="Add Word to Personal Vocabulary List"
      description="Modal to quick add vocab"
      ><QuickAddVocabForm ref="QuickAddVocabForm"
    /></Modal>
    <button type="button" class="btn btn-primary" @click="openModal">
      Quick Add Vocab
    </button>
  </div>
</template>
<script>
  import Modal from './components/Modal.vue';
  import QuickAddVocabForm from './components/QuickAddVocabForm.vue';

  export default {
    components: { Modal, QuickAddVocabForm },
    methods: {
      openModal() {
        this.$refs.Modal.toggleModal();
        this.$refs.QuickAddVocabForm.setFocus();
        this.$refs.QuickAddVocabForm.resetForm();
      },
    },
  };
</script>
