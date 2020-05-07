<template>
  <tr>
    <td>
      <strong>{{ text.title }}</strong>
      <span v-if="completed === 100" class="text-nav">
        <br>
        <a :href="`/lemmatized_text/${text.id}/`">Teacher</a>
        &bull;
        <a :href="`/lemmatized_text/${text.id}/learner/`">Learner</a>
      </span>
    </td>
    <td>{{ text.language }}</td>
    <td>
      <span v-if="completed === 100">{{ tokenCount }}</span>
      <div v-else class="progress-container">
        <div class="progress">
          <div class="progress-bar" :class="{'bg-warning': completed < 100}" role="progressbar" :style="`width: ${completed}%`" :aria-valuenow="completed" aria-valuemin="0" aria-valuemax="100" />
        </div>
        <div class="status">
          <small><a v-if="text.canRetry" href @click.prevent="onRetry">Retry</a></smalL>
          <small><a v-if="text.canCancel" href @click.prevent="onCancel">Cancel</a></smalL>
        </div>
      </div>
    </td>
    <td>
      <div v-if="text.stats" class="text-familiarity mb-0">
          <div class="familiarity-null">{{ text.stats.unranked }}</div>
          <div class="familiarity-1">{{ text.stats.one }}</div>
          <div class="familiarity-2">{{ text.stats.two }}</div>
          <div class="familiarity-3">{{ text.stats.three }}</div>
          <div class="familiarity-4">{{ text.stats.four }}</div>
          <div class="familiarity-5">{{ text.stats.five }}</div>
      </div>
    </td>
    <td>
      <a class="btn btn-outline-danger btn-sm" :href="text.deleteUrl"><i class="fa fa-trash" /> Delete</a>
      <a v-if="completed == 100" class="btn btn-outline-primary btn-sm" :href="text.cloneUrl"><i class="fa fa-copy" /> Clone</a>
    </td>
  </tr>
</template>

<script>
  import api from '../api';

  export default {
    props: {
      text: {
        type: Object,
        required: true,
      },
    },
    data() {
      return {
        completed: this.text.completed,
        tokenCount: this.text.tokenCount,
        lemmatizationStatus: this.text.lemmatizationStatus,
      };
    },
    created() {
      if (this.text.completed < 100) {
        this.updateStatus();
      }
    },
    methods: {
      updateStatus() {
        api.fetchTextStatus(this.text.id, (data) => {
          this.completed = data.data.completed;
          this.tokenCount = data.data.tokenCount;
          this.lemmatizationStatus = data.data.lemmatizationStatus;
          if (this.completed < 100 && ['finished', 'failed', 'queued'].indexOf(this.lemmatizationStatus) === -1) {
            setTimeout(this.updateStatus, 1000);
          }
        });
      },
      onRetry() {
        api.textRetryLemmatization(this.text.id, (data) => {
          this.completed = data.data.completed;
          this.tokenCount = data.data.tokenCount;
          if (this.completed < 100) {
            setTimeout(this.updateStatus, 1000);
          }
        });
      },
      onCancel() {
        api.textCancelLemmatization(this.text.id, (data) => {
          this.completed = data.data.completed;
          this.tokenCount = data.data.tokenCount;
        });
      },
    },
  };
</script>

<style lang="scss" scoped>
  td {
    vertical-align: middle;
  }
</style>
