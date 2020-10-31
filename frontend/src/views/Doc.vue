<template lang="pug">
.v-container.pa-4
  // Main content
  v-layout.text-left(column)
    h1 Методы
    h2 [Public] POST 
      code /api/get_preds/
    p Получить список рекомендаций
    h3 Параметры
    v-simple-table
      thead
        tr
          th Название
          th Тип
          th Обязательный параметр?
          th Описание
      tbody
        tr
          td user_id
          td Int
          td Нет
          td id_читателя из входного датасета, если не указать - выдаст рекомедации для неидентифицированного пользователя
    h3 Ответ
    p Объект с тремы полями:
      code { books: Book[], events: Event[], services: Service[] }
    h1 Обьекты
    h2 
      code Book
    p Обьект книги
    h3 Поля
    v-simple-table
      thead
        tr
          th Название
          th Тип
          th Обязательное поле?
          th Описание
      tbody
        tr
          td id
          td Int
          td Да
          td Уникальный идентфикатор книги
        tr
          td title
          td String
          td Нет
          td Название книги
        tr
          td author
          td String
          td Нет
          td Автор книги
        tr
          td publisher
          td String
          td Нет
          td Издатель книги
        tr
          td cover_url
          td String
          td Нет
          td URL-адрес обложки книги
        tr
          td year
          td Int
          td Нет
          td Год выпуска книги
        tr
          td age_rating
          td Int
          td Нет
          td Возрастное ограничение
    h2 
      code Event
    p Обьект мероприятия
    h3 Поля
    v-simple-table
      thead
        tr
          th Название
          th Тип
          th Обязательное поле?
          th Описание
      tbody
        tr
          td id
          td Int
          td Да
          td Уникальный идентфикатор мероприятия
        tr
          td name
          td String
          td Да
          td Название мероприятия
        tr
          td start_date
          td String
          td Да
          td Дата начала
        tr
          td end_date
          td String
          td Да
          td Дата окончания
        tr
          td description
          td String
          td Да
          td Описание мероприятия
        tr
          td address
          td String
          td Нет
          td Адрес мероприятия
        tr
          td age_limit
          td String
          td Да
          td Возрастное ограничение
        tr
          td age_group
          td String
          td Да
          td Рекомендуемый возраст вида "от 30 до 60 лет"
    h2 
      code Service
    p Обьект кружка
    h3 Поля
    v-simple-table
      thead
        tr
          th Название
          th Тип
          th Обязательное поле?
          th Описание
      tbody
        tr
          td id
          td Int
          td Да
          td Уникальный идентфикатор кружка
        tr
          td finance_type
          td String
          td Да
          td Платно/бесплатно
        tr
          td schedule_type
          td String
          td Да
          td Общее или индивидуальное занятие
        tr
          td service_name
          td String
          td Да
          td Название услуги
        tr
          td duration
          td Int
          td Да
          td Продолжительность
        tr
          td duration_unit
          td Strinf
          td Да
          td Единица измерения продолжительности (день, месяц, год и т.д.)
        tr
          td organization_name
          td String
          td Да
          td Название организации
        tr
          td organization_street_name
          td String
          td Нет
          td Адрес организации
        tr
          td organization_underground_name
          td String
          td Нет
          td Ближайшее метро к организации
        tr
          td service_class_name
          td String
          td Да
          td Имя класса сервиса (автошкола, танцы, музыка и т.д.)

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
export default class Doc extends Vue {
}
</script>

<style>
</style>
