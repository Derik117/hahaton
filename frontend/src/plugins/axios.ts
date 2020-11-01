import Vue from 'vue';
import VueAxios from 'vue-axios';
import axios from 'axios';
import store from '@/store';
import { SnackbarStore as _SnackbarStore } from '@/store';
import { getModule } from 'vuex-module-decorators';
let SnackbarStore = getModule(_SnackbarStore, store)
import { API_URI } from "@/main"
const instance = axios.create({
  baseURL: API_URI,
  timeout: 15000,
  headers: {
    'Accept': 'application/json',
    'Content-type': 'application/json',
  },
});
instance.interceptors.response.use((r: any) => {
  return r
}, (err: any) => {
  console.log(API_URI)
  let errText = err?.response?.data?.error || err.toString()
  SnackbarStore.setSnackbarError(errText);
  return Promise.reject(err);
})
Vue.use(VueAxios, instance);

export { instance as axios }