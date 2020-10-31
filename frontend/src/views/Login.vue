<template lang="pug">
.v-container.pa-4
  // Main content
  v-layout(align-center="" justify-center="")
    v-flex(xs12="" sm8="" md4="")
      v-form
        v-text-field(v-model="username" label="Login" name="login" prepend-icon="mdi-account-tie-outline" type="text")
        v-text-field#password(v-model="password" label="Password" name="password" prepend-icon="mdi-lock" type="password")
        v-spacer
        v-btn(color="primary" @click="login()") Login
</template>

<script lang="ts">
import Vue from 'vue'
import axios from 'axios'
import Component from 'vue-class-component'
import { i18n } from '@/plugins/i18n'
import { namespace } from 'vuex-class'
import { User } from '@/models/User'
const AppStore = namespace('AppStore')
const SnackbarStore = namespace('SnackbarStore')

@Component({
  components: {
  },
})
export default class Login extends Vue {
  @AppStore.Mutation setUser!: (user: User) => void
  @AppStore.Mutation setToken!: (token: string) => void
  @SnackbarStore.Mutation setSnackbarError!: (error: string) => void
  username: string = ""
  password: string = ""
  login() {
    return this.$auth.login({
      username: this.username,
      password: this.password,
    })
  }
}
</script>

<style>
</style>
