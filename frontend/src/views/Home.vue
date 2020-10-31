<template lang="pug">
.v-container.pa-4
  // Main content
  v-layout.text-center(column, justify-center, align-center)
    v-text-field(v-model="userId" label='user id')
    v-btn(@click="getPred" :loading="loading") Рекомендовать
    v-row(v-if="r.books.length")
      v-col(cols=4)
        div.text-h2 Книги
        v-card(v-for="b in r.books")
          v-list-item(three-line)
            v-list-item-content
              div.text-h6 {{b.title}}
                span(v-if="b.year") , {{b.year}}
              v-list-item-title {{b.author}}
              v-list-item-subtitle {{b.publisher}}
                span(v-if="b.age_rating") ({{b.age_rating}})
            v-list-item-avatar(tile, width="100", height="144")
              v-img(width="100px" :src="b.cover_url ? b.cover_url : 'https://via.placeholder.com/200x288?text=No+Cover'")
      v-col(cols=4)
        div.text-h2 Мероприятия
        v-card(v-for="e in r.events")
          v-list-item(three-line)
            v-list-item-content
              div.text-h6 {{e.name}} 
                span(v-if='e.age_limit') ({{e.age_limit}}+)
              v-list-item-title {{e.start_date}}
                span(v-if="e.start_date !== e.end_date")  - {{e.end_date}}
              span.text-left {{e.description}}
              v-list-item-subtitle.text-left(v-if="e.age_group") Рекомендуется {{e.age_group}} лет. 
              v-list-item-subtitle.text-left(v-if="e.address") ({{e.address}})
      v-col(cols=4)
        div.text-h2 Кружки
    //- span {{r.books ? r.books[0] : null }}
</template>

<script lang="ts">
import Vue from 'vue'
import {axios} from '@/plugins/axios'
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
  loading: boolean = false
  r: any = {books: [], events: [], services: []}
  getPred() {
    this.loading = true
    return axios.post('/api/get_preds/', {user_id: this.userId}).then(r => {
      this.r = r.data
    }).catch(err => {

    }).finally(() => {
      this.loading = false
    })
  }
}
</script>

<style>
</style>
