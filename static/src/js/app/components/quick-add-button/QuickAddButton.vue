<template>
  <div class="quick-add">
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
  import Modal from '../Modal.vue';
  import QuickAddVocabForm from './QuickAddVocabForm.vue';
  import { FETCH_ME } from '../../constants';

  export default {
    components: { Modal, QuickAddVocabForm },
    async created() {
      await this.$store.dispatch(FETCH_ME);
    },
    methods: {
      openModal() {
        this.$refs.Modal.toggleModal();
        this.$refs.QuickAddVocabForm.setFocus();
        this.$refs.QuickAddVocabForm.resetForm();
      },
    },
  };
</script>
