import Vue from 'vue';

import globalComponents from './components';
import store from './store';
import App from './App.vue';

Vue.config.productionTip = false;

export default () => {
  if (document.getElementById('app')) {
    globalComponents.forEach((component) => {
      Vue.component(component.name, component);
    });

    /* eslint-disable no-new */
    new Vue({
      el: '#app',
      render: h => h(App),
      store,
    });
  }
};
