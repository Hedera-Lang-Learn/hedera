<template>
  <div class="vocab-list row">
    <div class="col-8">
        <table class="table">
            <colgroup>
                <col style="width:20%">
                <col style="width:80%">
            </colgroup>
            <tr><th>Headword</th><th>Gloss</th></tr>
            <tr :class="{ 'selected-entry': selectedEntry && entry.id === selectedEntry.id }" v-for="entry in entries" :key="entry.id">
                <td @click="selectEntry(entry)">{{ entry.headword }}</a></td>
                <td>{{ entry.gloss }}</td>
            </tr>
        </table>
    </div>
    <div class="col-4">
        <LatticeNode :node="selectedNode" @selected="onSelect" />
    </div>
  </div>
</template>

<script>
  import api from './api';
  import LatticeNode from "./modules/LatticeNode.vue";
  import { FETCH_NODE } from './constants';

  const prevIndex = (currentIndex, tokens) => {
    let index = (currentIndex || 0) - 1;
    if (index === -1) {
        index = tokens.length - 1;
    }
    return index;
  }

  const nextIndex = (currentIndex, tokens) => {
    let index = (currentIndex || -1) + 1;
    if (index === tokens.length) {
        index = 0;
    }
    return index;
  }

  export default {
    props: ['vocabId'],
    components: { LatticeNode },
    data() {
      return {
        selectedEntry: null,
        selectedNode: null,
        entries: [],
      }
    },
    shortcuts: {
      prevVocabEntry() {
        this.goToWord(prevIndex);
      },
      nextVocabEntry() {
        this.goToWord(nextIndex);
      },
    },
    computed: {
      selectedIndex() {
        if (this.selectedEntry) {
          return this.entries.indexOf(this.selectedEntry);
        }
      }
    },
    methods: {
      goToWord(indexFunction) {
        const index = indexFunction(this.selectedIndex, this.entries);
        this.selectEntry(this.entries[index]);
      },
      selectEntry(entry) {
          this.selectedEntry = entry;
          if (entry.node === null) {
            this.selectedNode = null;
            return;
          }
          if (this.$store.state.nodes[entry.node] && this.$store.state.nodes[entry.node].id) {
            this.selectedNode = this.$store.state.nodes[entry.node];
          } else {
            this.$store.dispatch(FETCH_NODE, {id: entry.node}).then(() => {
              this.selectedNode = this.$store.state.nodes[entry.node];
            });
          }
      },
      onSelect(node) {
        console.log('select', node);
      },
    },
    watch: {
      vocabId: {
        immediate: true,
        handler() {
          api.fetchVocabEntries(this.vocabId, data => {
            this.entries = data.data;
          });
        }
      },
    },
  }
</script>

<style lang="scss" scoped>
  tr {
      border-left: 3px solid transparent;
  }
  tr.selected-entry {
      border-left-color: #444;
      background: #EFEFEF;
  }
</style>
