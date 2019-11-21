import Vue from 'vue';
import VueKeybindings from 'vue-keybindings';

import globalComponents from './components';
import store from './store';
import App from './App.vue';
import Learner from './Learner.vue';
import PersonalVocab from './PersonalVocab.vue';
import Vocab from './Vocab.vue';

Vue.config.productionTip = false;

export default () => {
  if (document.getElementById('app')) {
    globalComponents.forEach((component) => {
      Vue.component(component.name, component);
    });

    Vue.use(VueKeybindings, {
      alias: {
        prevWord: ['arrowleft'],
        nextWord: ['arrowright'],
        prevUnresolved: ['shift', 'arrowleft'],
        nextUnresolved: ['shift', 'arrowright'],
      },
    });

    /* eslint-disable no-new */
    new Vue({
      el: '#app',
      render(h) {
        return h(App, { props: { textId: store.state.textId || this.$el.attributes['text-id'].value } });
      },
      store,
    });
  }

  if (document.getElementById('learner-app')) {
    globalComponents.forEach((component) => {
      Vue.component(component.name, component);
    });

    Vue.use(VueKeybindings, {
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
    });

    /* eslint-disable no-new */
    new Vue({
      el: '#learner-app',
      render(h) {
        return h(Learner, { props: { textId: store.state.textId || this.$el.attributes['text-id'].value } });
      },
      store,
    });
  }

  if (document.getElementById('personal-vocab-app')) {
    globalComponents.forEach((component) => {
      Vue.component(component.name, component);
    });

    /* eslint-disable no-new */
    new Vue({
      el: '#personal-vocab-app',
      render(h) {
        return h(PersonalVocab, { props: { lang: this.$el.attributes.lang.value } });
      },
      store,
    });
  }

  if (document.getElementById('vocab-app')) {
    globalComponents.forEach((component) => {
      Vue.component(component.name, component);
    });

    Vue.use(VueKeybindings, {
      alias: {
        nextVocabEntry: ['shift', 'arrowdown'],
        prevVocabEntry: ['shift', 'arrowup'],
      },
    });

    /* eslint-disable no-new */
    new Vue({
      el: '#vocab-app',
      render(h) {
        return h(Vocab, { props: { vocabId: this.$el.attributes.vocabId.value } });
      },
      store,
    });
  }
};
