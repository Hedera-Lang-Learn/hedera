<template>
  <div>
    <div
      class="modal fade"
      :class="{ show, 'd-block': active }"
      tabindex="-1"
      role="dialog"
      @keyup.esc.stop="toggleModal"
    >
      <div class="modal-dialog" role="document" :aria-labelledby="title" :aria-describedby="description">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{title}}</h5>
            <button
              ref="modal"
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="toggleModal"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <div class="form-group">
            <slot></slot>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="active" class="modal-backdrop fade show"></div>
  </div>
</template><script>

  export default {
    props: ['title', 'description'],
    data() {
      return {
        active: false,
        show: false,
      };
    },
    methods: {
      /**
       * when clicking on button in bootstrap
       * the modal style set to display and after that a show class add to modal
       * so to do that we will show modal-backdrop and set modal display to block
       * then after that we will add show class to the modal and we will use setTimeout
       * to add show class because we want show class to add after the modal-backdrop show and modal display change
       * to make modal animation work
       * */
      toggleModal() {
        const body = document.querySelector('body');
        this.active = !this.active;
        if (this.active) {
          body.classList.add('modal-open');
        } else {
          body.classList.remove('modal-open');
        }
        // mainly for smooth animation as noted above
        setTimeout(() => { this.show = !this.show; }, 10);
      },
    },
  };
</script>
