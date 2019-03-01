import Vue from 'vue';
import VueKeybindings from 'vue-keybindings';

import globalComponents from './components';
import store from './store';
import App from './App.vue';

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
};
