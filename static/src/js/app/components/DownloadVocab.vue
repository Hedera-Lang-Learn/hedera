<template>
  <a class="btn btn-sm btn-light" :href="VocabListDownload" download="personal_vocab_list.csv">
    <i class="fa fa-fw fa-download" aria-hidden="true" /> Export
  </a>
</template>

<script>
  const toCSV = (data) => {
    if (data.length === 0) {
      return null;
    }

    let result; let
      ctr;
    const columnDelimiter = ',';
    const lineDelimiter = '\n';
    const keys = Object.keys(data[0]);

    result = '';
    result += keys.join(columnDelimiter);
    result += lineDelimiter;

    data.forEach((item) => {
      ctr = 0;
      keys.forEach((key) => {
        if (ctr > 0) {
          result += columnDelimiter;
        }
        result += `"${item[key]}"`;
        ctr += 1;
      });
      result += lineDelimiter;
    });

    return result;
  };

  export default {
    props: ['glosses', 'withFamiliarity'],
    computed: {
      personalVocabList() {
        return this.$store.state.personalVocabList;
      },
      VocabListDownload() {
        const vocabList = this.glosses;
        const data = toCSV(vocabList.map((entry) => {
          const row = {
            headword: entry.headword,
            definition: entry.definition,
            lemma_id: entry.lemma
          };
          if (this.withFamiliarity) {
            row.familiarity = entry.familiarity;
            // const entry = this.personalVocabList.entries.filter((e) => e.node === g.node);
            // row.familiarity = (entry[0] && entry[0].familiarity) || '';
          }
          return row;
        }));
        return data === null ? null : encodeURI(`data:text/csv;charset=utf-8,${data}`);
      },
    },
  };
</script>

<style lang="scss" scoped>

</style>
