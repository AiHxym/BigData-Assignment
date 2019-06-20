import Vue from 'vue'
import App from './App.vue'
import router from './router'
import iView from 'iview';
import 'iview/dist/styles/iview.css';
import echarts from 'echarts'

Vue.prototype.$echarts = echarts

require('echarts-wordcloud')
Vue.use(iView);
Vue.config.productionTip = false

new Vue({
  router,
  render: function (h) { return h(App) }
}).$mount('#app')
