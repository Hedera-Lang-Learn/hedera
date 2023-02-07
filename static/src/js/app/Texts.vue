<template>
  <div class="lemmatized-texts mb-4">
    <div class="card">
      <div class="card-header d-flex justify-content-between">
        <ul class="nav nav-tabs card-header-tabs">
          <li class="nav-item" role="presentation">
            <a class="nav-link" :class="{ active: ownSelected }" href @click.prevent="selected = 'own-texts'">Original Texts</a>
          </li>
          <li class="nav-item" role="presentation">
            <a class="nav-link" :class="{ active: classSelected }" href @click.prevent="selected = 'class-texts'">Class Texts</a>
          </li>
        </ul>

        <a v-if="ownSelected" class="btn btn-primary btn-sm" href="/lemmatized_text/create/"><i class="fa fa-plus" aria-hidden="true"></i> Create</a>
      </div>
      <div class="tab-content">
        <div class="tab-pane fade show active">
          <table class="table">
            <tr><th>Text</th><th>Language</th><th>Length</th><th>Created At</th><th v-if="ownSelected" /><th v-else>Familiarity</th></tr>
            <TextRow
              v-for="text in activeTexts"
              :key="text.id"
              :text="text"
              :teacherMode="ownSelected"
            />
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import TextRow from './components/TextRow.vue';
  import { PROFILE_FETCH, LEMMATIZED_TEXT_FETCH_LIST } from './constants';

  export default {
    components: {
      TextRow,
    },
    data() {
      return {
        selected: 'own-texts',
      };
    },
    computed: {
      ownSelected() {
        return this.selected === 'own-texts';
      },
      classSelected() {
        return this.selected === 'class-texts';
      },
      activeTexts() {
        return this.ownSelected ? this.ownTexts : this.groupTexts;
      },
      ownTexts() {
        return this.$store.state.texts.filter((text) => text.clonedFor === null);
      },
      groupTexts() {
        return this.$store.state.texts.filter((text) => text.clonedFor !== null);
      },
    },
    created() {
      this.$store.dispatch(PROFILE_FETCH);
      this.$store.dispatch(LEMMATIZED_TEXT_FETCH_LIST);
    },
  };
</script>

<style lang="scss" scoped>

</style>
