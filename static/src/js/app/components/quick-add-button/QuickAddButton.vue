<template>
  <div class="quick-add">
    <Modal
      ref="Modal"
      title="Add Word to Personal Vocabulary List"
      description="Modal to quick add vocab"
      >
        <QuickAddVocabForm ref="QuickAddVocabForm" :current-lang-tab="currentLangTab"/>
      </Modal>
    <button type="button" class="btn btn-primary" @click="openModal">
      Quick Add Vocab
    </button>
  </div>
</template>
<script>
  import Modal from '../Modal.vue';
  import QuickAddVocabForm from './QuickAddVocabForm.vue';

  export default {
    components: { Modal, QuickAddVocabForm },
    props: ['currentLangTab'],
    methods: {
      openModal() {
        this.$refs.Modal.toggleModal();
        this.$refs.QuickAddVocabForm.setFocus();
        this.$refs.QuickAddVocabForm.resetForm();
      },
    },
  };
</script>
