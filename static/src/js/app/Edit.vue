<template>
  <div class="edit-container">
    <div class="row">
      <div class="col-8">
        <h1>Hey Ho</h1>
        <!-- <ckeditor :editor="editor" v-model="editorData" :config="editorConfig"></ckeditor> -->
        <!-- {{ this.transformedTokens }} -->
      </div>
    </div>
  </div>
</template>

<script>
  // import { CKEditor, ClassicEditor } from './editor/ckeditor';
  // import ClassicEditor from './editor/ckeditor';
  // import ConvertSpanAttributes from './editor/plugins';
  // import GeneralHtmlSupport from '@ckeditor/ckeditor5-html-support/src/generalhtmlsupport';
  // import HederaEditor from './editor/hederaEditor';
  import {
    FETCH_ME,
    FETCH_TEXT,
    FETCH_PERSONAL_VOCAB_LIST,
    FETCH_TOKENS,
  } from './constants';

  // const hederaEditor = ClassicEditor
  //   .create(document.querySelector('#editor'), {
  //     extraPlugins: [ConvertSpanAttributes],
  //   })
  //   .then((editor) => {
  //     console.log('Editor was initialized', editor);
  //   })
  //   .catch((err) => {
  //     console.error(err.stack);
  //   });

  export default {
    props: ['textId'],
    components: {
      ckeditor: CKEditor.component,
    },
    data() {
      return {
        // editor: ClassicEditor,
        editorData: '',
        editorConfig: {
          toolbar: 'Custom',
          toolbar_Custom: [],
          // plugins: [GeneralHtmlSupport],
          htmlSupport: {
            allow: [
              {
                name: 'span',
                classes: true,
                attributes: true,
              },
            ],
          },
        },
      };
    },
    created() {
      this.$store.dispatch(FETCH_ME);
    },
    watch: {
      textId: {
        immediate: true,
        handler() {
          this.$store.dispatch(FETCH_TEXT, { id: this.textId }).then(() => this.$store.dispatch(FETCH_PERSONAL_VOCAB_LIST, { lang: this.text.lang }));
        },
      },
      selectedVocabList: {
        immediate: true,
        handler() {
          this.$store.dispatch(FETCH_TOKENS, { id: this.textId, personalVocabList: this.selectedVocabList });
        },
      },
      tokens: {
        immediate: true,
        handler() {
          this.transormTokensToEditableHTML(this.tokens);
        },
      },
    },
    methods: {
      transormTokensToEditableHTML(tokens) {
        const tokenHTML = tokens.map((token) => (
          `<span node=${token.node} resolved=${token.resolved} previously-lemmatized="true">
          ${token.word}
          </span>${token.following ? `<span class="following" >${token.following}</span>` : ''}`
        )).join('');
        // tokens.forEach((t) => {
        //   if (t.following == '\r\n\r\n') {
        //     console.log('True');
        //   } else {
        //     console.log('False');
        //   }
        // });
        // const tokenHTML = tokens.map((token) => token.word).join(' ');

        this.editorData = tokenHTML;
        return this.editorData;
      },
    },
    computed: {
      tokens() {
        return this.$store.state.tokens;
      },
    },
  };
</script>

<style lang="scss" scoped>

</style>
