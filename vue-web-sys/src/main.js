import 'babel-polyfill'
import 'es6-promise/auto'
import promise from 'es6-promise'
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui'
import './assets/scss/style.scss'
import 'element-ui/lib/theme-chalk/index.css'
import VueParticles from 'vue-particles'
 

promise.polyfill()
 
Vue.config.productionTip = false
Vue.use(VueParticles)
Vue.use(ElementUI)

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app')