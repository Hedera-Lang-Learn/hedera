<template>
  <tr>
    <td>
      <strong v-if="completed < 100">{{ text.title }}</strong>
      <a v-else :href="textUrl">{{ text.title }}</a>
    </td>
    <td>{{ text.language }}</td>
    <td>
      <span v-if="completed === 100">{{ tokenCount }}</span>
      <div v-else class="progress-container">
        <div class="progress">
          <div
            class="progress-bar"
            :class="{ 'bg-warning': completed < 100 }"
            role="progressbar"
            :style="`width: ${completed}%`"
            :aria-valuenow="completed"
            aria-valuemin="0"
            aria-valuemax="100"
          />
        </div>
        <div class="status" v-if="teacherMode">
          <small
            ><a v-if="text.canRetry" href @click.prevent="onRetry"
              >Retry</a
            ></small
          >
          <small
            ><a v-if="text.canCancel" href @click.prevent="onCancel"
              >Cancel</a
            ></small
          >
        </div>
      </div>
    </td>
    <td>
      {{
        this.$options.filters.dateFormat(this.$data.createdAt, 'MMM D, YYYY')
      }}
    </td>
    <td v-if="teacherMode">
      <a class="btn btn-outline-danger btn-sm" :href="text.deleteUrl"
        ><i class="fa fa-trash" aria-hidden="true" /> Delete</a
      >
      <a
        v-if="completed == 100"
        class="btn btn-outline-primary btn-sm"
        :href="text.cloneUrl"
        ><i class="fa fa-copy" aria-hidden="true" /> Clone</a
      >
      <a
        v-if="completed == 100"
        class="btn btn-outline-info btn-sm"
        :href="text.editUrl"
        ><i class="fa fa-edit" aria-hidden="true" /> Edit</a
      >
    </td>
    <td v-else>
      <div v-if="text.stats" class="text-familiarity mb-0">
        <div class="familiarity-null">{{ text.stats.unranked }}</div>
        <div class="familiarity-1">{{ text.stats.one }}</div>
        <div class="familiarity-2">{{ text.stats.two }}</div>
        <div class="familiarity-3">{{ text.stats.three }}</div>
        <div class="familiarity-4">{{ text.stats.four }}</div>
        <div class="familiarity-5">{{ text.stats.five }}</div>
      </div>
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
    teacherMode: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    textUrl() {
      return this.teacherMode
        ? `/lemmatized_text/${this.text.id}/`
        : `/lemmatized_text/${this.text.id}/learner/`;
    },
  },
  data() {
    return {
      completed: this.text.completed,
      createdAt: new Date(this.text.createdAt),
      tokenCount: this.text.tokenCount,
      lemmatizationStatus: this.text.lemmatizationStatus,
      public: this.text.public,
    };
  },
  created() {
    if (this.text.completed < 100) {
      this.updateStatus();
    }
  },
  methods: {
    // can you update read status here? maybe 3 options - read, in progress, unread
    async updateStatus() {
      const response = await api.lemmatizedText_fetchStatus(this.text.id);
      const { data } = response.data;
      const { completed, tokenCount, lemmatizationStatus } = data;
      this.completed = completed;
      this.tokenCount = tokenCount;
      this.lemmatizationStatus = lemmatizationStatus;
      if (
        this.completed < 100 &&
        ['finished', 'failed', 'queued'].indexOf(this.lemmatizationStatus) ===
          -1
      ) {
        setTimeout(this.updateStatus, 1000);
      }
    },
    async onRetry() {
      const response = await api.lemmatizedText_retry(this.text.id);
      const { data } = response.data;
      const { completed, tokenCount } = data;
      this.completed = completed;
      this.tokenCount = tokenCount;
      if (this.completed < 100) {
        setTimeout(this.updateStatus, 1000);
      }
    },
    async onCancel() {
      const response = await api.lemmatizedText_cancel(this.text.id);
      const { data } = response.data;
      const { completed, tokenCount } = data;
      this.completed = completed;
      this.tokenCount = tokenCount;
    },
  },
};
</script>

<style lang="scss" scoped>
td {
  vertical-align: middle;
}
.progress-bar {
  transition: width 0.5s ease;
}
</style>
