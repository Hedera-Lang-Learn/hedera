<template>
  <div class="vocab-list" v-if="loading">
    <p class="lead">Loading...</p>
  </div>
  <div class="vocab-list row" v-else>
    <div class="col-8">
        <VocabListTable @selectEntry="onSelectEntry" :entries="entries" :selected-index="selectedIndex" />
    </div>
    <div class="col-4">
        <div style="position: fixed;">
          <LatticeNode :node="selectedNode" @selected="onSelectNode" />
        </div>
    </div>
  </div>
</template>

<script>
  import api from './api';
  import LatticeNode from './modules/LatticeNode.vue';
  import VocabListTable from './components/vocab-list-table';
  import { FETCH_NODE } from './constants';

  export default {
    props: ['vocabId'],
    components: { LatticeNode, VocabListTable },
    data() {
      return {
        selectedEntry: null,
        selectedNode: null,
        entries: [],
        loading: false,
      };
    },
    computed: {
      selectedIndex() {
        return this.selectedEntry ? this.entries.findIndex((e) => e.id === this.selectedEntry.id) : null;
      },
    },
    methods: {
      onSelectEntry(entry) {
        this.selectedEntry = entry;
        this.selectNode(entry.node);
      },
      selectNode(nodePK) {
        if (nodePK === null) {
          this.selectedNode = null;
          return;
        }
        if (this.$store.state.nodes[nodePK] && this.$store.state.nodes[nodePK].id) {
          this.selectedNode = this.$store.state.nodes[nodePK];
        } else {
          this.$store.dispatch(FETCH_NODE, { id: nodePK }).then(() => {
            this.selectedNode = this.$store.state.nodes[nodePK];
          });
        }
      },
      onSelectNode(node) {
        api.vocabEntryLink(this.selectedEntry.id, node.pk, (data) => {
          this.entries.splice(this.selectedIndex, 1, data);
          this.selectNode(node.pk);
        });
      },
    },
    watch: {
      vocabId: {
        immediate: true,
        handler() {
          this.loading = true;
          api.fetchVocabEntries(this.vocabId, (data) => {
            this.entries = data.data;
            this.loading = false;
          });
        },
      },
    },
  };
</script>

<style lang="scss" scoped>
</style>
