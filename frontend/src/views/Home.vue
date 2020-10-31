<template lang="pug">
.v-container.pa-4
  // Main content
  v-layout.text-center(column, justify-center, align-center)
    v-text-field(v-model="userId" label='user id')
    v-btn(@click="getPred") Load
    v-row
      v-col(v-for="b in r.books")
        v-card(width=350)
          v-list-item(three-line)
            v-list-item-content
              div.text-h6 {{b.title}}
                span(v-if="b.year") , {{b.year}}
              v-list-item-title {{b.author}}
              v-list-item-subtitle {{b.publisher}}
                span(v-if="b.age_rating") ({{b.age_rating}})
            v-list-item-avatar(tile, width="100", height="144")
              v-img(width="100px" :src="b.cover_url ? b.cover_url : 'https://via.placeholder.com/200x288?text=Нет+Обложки'")
    //- span {{r.books ? r.books[0] : null }}
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
export default class Home extends Vue {
  @AppStore.Mutation setUser!: (user: User) => void
  @SnackbarStore.Mutation setSnackbarError!: (error: string) => void
  userId: number = 1
  r: any = {books: []}
  getPred() {
    return axios.post('/api/get_preds/', {user_id: this.userId}).then(r => {
      this.r = r.data
    })
  }
}
</script>

<style>
</style>
