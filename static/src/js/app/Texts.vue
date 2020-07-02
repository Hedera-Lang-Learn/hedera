<template>
  <div class="lemmatized-texts mb-4">
    <div class="card">
      <div class="card-header">
        <ul class="nav nav-tabs card-header-tabs">
          <li class="nav-item" role="presentation">
            <a class="nav-link" :class="{ active: selected === 'own-texts' }" href @click.prevent="selected = 'own-texts'">Original Texts</a>
          </li>
          <li class="nav-item" role="presentation">
            <a class="nav-link" :class="{ active: selected === 'class-texts' }" href @click.prevent="selected = 'class-texts'">Class Texts</a>
          </li>
        </ul>
      </div>
      <div class="tab-content">
        <div class="tab-pane fade show active">
          <table class="table">
            <tr><th>Text</th><th>Language</th><th>Length</th><th>Familiarity</th><th /></tr>
            <TextRow
              v-for="text in activeTexts"
              :key="text.id"
              :text="text"
            />
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import api from './api';

  import TextRow from './components/TextRow.vue';

  export default {
    components: {
      TextRow,
    },
    data() {
      return {
        texts: [],
        selected: 'own-texts',
      };
    },
    computed: {
      activeTexts() {
        return this.selected === 'own-texts' ? this.ownTexts : this.groupTexts;
      },
      ownTexts() {
        return this.texts.filter(text => text.clonedFor === null);
      },
      groupTexts() {
        return this.texts.filter(text => text.clonedFor !== null);
      }
    },
    created() {
      api.fetchTexts((data) => {
        this.texts = data.data.map((datum) => ({
          ...datum.text,
          stats: datum.stats,
        }));
      });
    },
  };
</script>

<style lang="scss" scoped>

</style>
