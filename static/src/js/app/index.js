import Vue from 'vue';
import VueKeybindings from 'vue-keybindings';

import globalComponents from './components';
import store from './store';

import App from './App.vue';
import Learner from './Learner.vue';
import PersonalVocab from './PersonalVocab.vue';
import Vocab from './Vocab.vue';
import Texts from './Texts.vue';
import Dashboard from './Dashboard.vue';
import QuickAddButton from './components/quick-add-button';

Vue.config.productionTip = false;

const loadGlobals = () => {
  globalComponents.forEach((component) => {
    Vue.component(component.name, component);
  });
};

const load = (appId, appComponent, keyBindingsConfig, appProps) => {
  if (document.getElementById(appId)) {
    loadGlobals();

    if (keyBindingsConfig !== null) {
      Vue.use(VueKeybindings, keyBindingsConfig);
    }

    /* eslint-disable no-new */
    new Vue({
      el: `#${appId}`,
      render(h) {
        return h(appComponent, { props: appProps(this.$el) });
      },
      store,
    });
  }
};

const appKeyBindings = {
  alias: {
    prevWord: ['arrowleft'],
    nextWord: ['arrowright'],
    prevUnresolved: ['shift', 'arrowleft'],
    nextUnresolved: ['shift', 'arrowright'],
  },
};
const learnerKeyBindings = {
  alias: {
    prevWord: ['arrowleft'],
    nextWord: ['arrowright'],
    prevUnresolved: ['shift', 'arrowleft'],
    nextUnresolved: ['shift', 'arrowright'],
    one: ['1'],
    two: ['2'],
    three: ['3'],
    four: ['4'],
    five: ['5'],
  },
};
const vocabAppKeyBindings = {
  alias: {
    nextVocabEntry: ['arrowright'],
    prevVocabEntry: ['arrowleft'],
  },
};
const textAppProps = ($el) => ({ textId: store.state.textId || $el.attributes['text-id'].value });
const personalVocabAppProps = ($el) => ({ lang: $el.attributes.lang.value });
const vocabAppProps = ($el) => ({ vocabId: $el.attributes.vocabId.value });

export default () => {
  load('app', App, appKeyBindings, textAppProps);
  load('learner-app', Learner, learnerKeyBindings, textAppProps);
  load('personal-vocab-app', PersonalVocab, null, personalVocabAppProps);
  load('vocab-app', Vocab, vocabAppKeyBindings, vocabAppProps);
  load('texts-app', Texts, null, () => {});
  load('dashboard-app', Dashboard, null, () => {});
  load('quick-add', QuickAddButton, null, () => {});
};
