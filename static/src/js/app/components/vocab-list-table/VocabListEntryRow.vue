<template>
  <tbody v-if="deleting" class="alert alert-danger">
    <tr :class="{ 'selected-entry': selected }">
      <td>{{ entry.headword }}</td>
      <td>{{ entry.definition }}</td>
      <td v-if="showIds">{{ entry.lemma }}</td>
      <td>
      </td>
    </tr>
    <tr>
      <td colspan="4" v-if="saving"><span class="saving">Deleting...</span></td>
      <td colspan="4" v-else>
        <p>Are you are sure you want to delete this vocab entry?</p>
        <div class="d-flex justify-content-between">
          <a class="btn btn-sm btn-danger" @click.prevent="onDeleteConfirm"><i class="fa fa-fw fa-trash" aria-hidden="true"  /> Yes, Delete</a>
          <a class="btn btn-light btn-sm cancel-entry" href @click.prevent="onCancel"><i class="fa fa-fw fa-ban" aria-hidden="true" /> No, Cancel</a>
        </div>
      </td>
    </tr>
  </tbody>
  <tr v-else-if="editing" :class="{ 'selected-entry': selected }">
    <td><input class="form-control" v-model="model.headword" /></td>
    <td><input class="form-control" v-model="model.definition" /></td>
    <td>{{ entry.lemma }}</td>
    <td>
      <span class="saving" v-if="saving">Saving...</span>
      <div class="btn-group text-nowrap" v-else>
        <a class="btn btn-primary btn-sm" href @click.prevent="onSave"><i class="fa fa-fw fa-check" aria-hidden="true" /> Save</a>
        <a class="btn btn-light btn-sm" href @click.prevent="onCancel"><i class="fa fa-fw fa-ban" aria-hidden="true" /> Cancel</a>
      </div>
    </td>
  </tr>
  <tr v-else :class="{ 'selected-entry': selected }">
    <td>
      <a href @click.prevent="$emit('select-entry', entry)">{{ entry.headword }}</a>
    </td>
    <td>{{ entry.definition }}</td>
    <td v-if="showIds">{{ entry.lemma }}</td>
    <td>
      <div class="btn-group" v-if='canEdit'>
        <a class="btn btn-light btn-sm delete-entry" href @click.prevent="onDelete"><i class="fa fa-fw fa-trash" aria-hidden="true" title="Delete Entry" /><span class="sr-only">Delete Entry</span></a>
        <a class="btn btn-light btn-sm edit-entry" href @click.prevent="onEdit"><i class="fa fa-fw fa-pen-fancy" aria-hidden="true" title="Edit Entry" /><span class="sr-only">Edit Entry</span></a>
      </div>
    </td>
  </tr>
</template>

<script>
  export default {
    props: ['entry', 'selected', 'showIds', 'canEdit'],
    data() {
      return {
        saving: false,
        deleting: false,
        editing: false,
        model: {
          headword: this.entry.headword,
          definition: this.entry.definition,
        },
      };
    },
    watch: {
      entry: {
        immediate: true,
        handler() {
          const { headword, definition } = this.entry;
          this.model = {
            ...this.model,
            headword,
            definition,
          };
        },
      },
    },
    methods: {
      onDelete() {
        this.deleting = true;
        this.editing = false;
      },
      onEdit() {
        this.deleting = false;
        this.editing = true;
      },
      resetFlags() {
        this.deleting = false;
        this.editing = false;
        this.saving = false;
      },
      onDeleteConfirm() {
        this.saving = true;
        this.$emit('delete-entry', {
          entry: this.entry,
          cb: this.resetFlags,
        });
      },
      onSave() {
        this.saving = true;
        this.$emit('edit-entry', {
          entry: this.entry,
          headword: this.model.headword,
          definition: this.model.definition,
          cb: this.resetFlags,
        });
      },
      onCancel() {
        this.resetFlags();
      },
    },
  };
</script>

<style lang="scss" scoped>
  @import '../../../../scss/config';
  tr {
      border-left: 3px solid transparent;
  }
  tr.selected-entry {
      border-left-color: #444;
      background: #EFEFEF;
  }
  .btn-group {
    .delete-entry:hover {
      color: $danger;
    }
    .edit-entry:hover {
      color: $blue;
    }
  }
  .btn-danger {
    color: $white;
  }
</style>
