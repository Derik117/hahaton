let API_URI = process.env.VUE_APP_API_URI

import Vue from 'vue'
import App from '@/App.vue'
import router from '@/plugins/router'
import VueAuth from '@d0whc3r/vue-auth-plugin';
import store from '@/store'
import { i18n } from '@/plugins/i18n'
import vuetify from '@/plugins/vuetify'
import '@/plugins/axios'

(Vue as any).store = store;
(Vue as any).router = router;


Vue.use(VueAuth, {
  vuexStoreSpace: 'AppCode',
  authRedirect: '/login',
  loginData: { url: '/auth/login/', method: 'POST', redirect: '/', headerToken: 'Authorization', fetchUser: true, customToken: (r: any) => r.data.token },
  logoutData: { redirect: '/login' },
  fetchData: { url: '/auth/profile/', method: 'GET', interval: 30, enabled: true },
})
Vue.config.productionTip = true
let app = new Vue({
  router,
  store,
  i18n,
  vuetify,
  render: (h) => h(App),
}).$mount('#app')
// @ts-expect-error
app.API_URI = API_URI
// @ts-expect-error
global.app = app
export { API_URI }