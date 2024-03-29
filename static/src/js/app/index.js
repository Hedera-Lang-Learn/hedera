import Vue from 'vue';
import VueKeybindings from 'vue-keybindings';
import VueFilterDateFormat from '@vuejs-community/vue-filter-date-format';
import VueGoodTablePlugin from 'vue-good-table';
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue';
import 'vue-good-table/dist/vue-good-table.css';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

import globalComponents from './components';
import store from './store';

import App from './App.vue';
import Learner from './Learner.vue';
import PersonalVocab from './PersonalVocab.vue';
import Texts from './Texts.vue';
import Dashboard from './Dashboard.vue';
// import QuickAddButton from './components/quick-add-button';

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

    Vue.use(VueFilterDateFormat);
    Vue.use(VueGoodTablePlugin);
    Vue.use(BootstrapVue);
    Vue.use(IconsPlugin);

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
const textAppProps = ($el) => ({ textId: store.state.textId || $el.attributes['text-id'].value });
const vocabAppProps = ($el) => ({
  // default to null due to undefined error
  vocabId: $el.attributes.vocabId.value || null,
  lang: $el.attributes.lang.value,
  personalVocab: $el.attributes.personalVocab.value === 'true',
});

export default () => {
  load('app', App, appKeyBindings, textAppProps);
  load('learner-app', Learner, learnerKeyBindings, textAppProps);
  load('personal-vocab-app', PersonalVocab, null, vocabAppProps);
  load('vocab-app', PersonalVocab, null, vocabAppProps);
  load('texts-app', Texts, null, () => {});
  load('dashboard-app', Dashboard, null, () => {});
  // Removed for now - buggy - modal window should not be a child of dropdown-content
  // load('quick-add', QuickAddButton, null, () => ({
  //   personalVocab: true,
  // }));
};
