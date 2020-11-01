# -*- coding: utf-8 -*-
import random

import telebot
from telebot import types
import os
import datetime as dt
import requests
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist
from hahaton.utils import activate_django_env
activate_django_env()
from data.models.reader import Reader
from data.models.bot_user import BotUser
from data.models.catalog import Catalog
from data.models.quote import Quote

token = os.environ.get('tg_bot_token')
bot = telebot.TeleBot(token)


def calculate_age(born):
    today = dt.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

@bot.message_handler(commands=["start"])
def welcome(message):
    user_id = message.from_user.id
    try:
        BotUser.objects.get(tg_id=user_id)
        mainmenu(message)
    except ObjectDoesNotExist:
        text = """
        Добро пожаловать!\nЭтот бот создан для того чтобы посоветовать вам интересную книгу для прочтения.\n\nНо для начала нам нужно познакомиться.\nВы уже зарегестрированы в системе?\nОтвечайте "Да" или "Нет"
        """
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('Да', 'Нет')
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, process_step)


def process_step(message):
    chat_id = message.chat.id
    if message.text == 'Да':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add('Назад')
        msg = bot.send_message(chat_id, 'Отлично, тогда укажите reader_id', reply_markup=markup)
        bot.register_next_step_handler(msg, get_reader_id)
    elif message.text == 'Нет':
        text = "Тогда давайте знакомиться!\nДля регистрации в системе мне необходима ваша дата рождения в формате 'День.Месяц.Год'\n\nНапример: 09.09.1999"
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add('Назад')
        msg = bot.send_message(chat_id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, register)
    else:
        msg = bot.send_message(chat_id, 'Отвечайте "Да" или "Нет"')
        bot.register_next_step_handler(msg, process_step)


def register(message):
    if message.text == 'Назад':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('Да', 'Нет')
        msg = bot.send_message(message.chat.id, "Вы уже зарегестрированы?", reply_markup=markup)
        bot.register_next_step_handler(msg, process_step)
        return
    try:
        date = dt.datetime.strptime(message.text, '%d.%m.%Y')
        reader = Reader.objects.create(birth_date=date, age=calculate_age(date))
        user_id = message.from_user.id
        BotUser.objects.create(reader=reader, tg_id=user_id)
        bot.send_message(message.chat.id, "Регистрация прошла успешно!")
        mainmenu(message)
    except ValueError:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add('Назад')
        msg = bot.send_message(message.chat.id, "Пожалуйста, отправляйте корректную дату в формате 'День.Месяц.Год'", reply_markup=markup)
        bot.register_next_step_handler(msg, register)


def get_reader_id(message):
    if message.text == 'Назад':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('Да', 'Нет')
        msg = bot.send_message(message.chat.id, "Вы уже зарегестрированы?", reply_markup=markup)
        bot.register_next_step_handler(msg, process_step)
        return
    try:
        reader_object = Reader.objects.get(id=message.text)
        user_id = message.from_user.id
        BotUser.objects.create(reader=reader_object, tg_id=user_id)
        bot.send_message(message.chat.id, "Авторизация прошла успешно!")
        mainmenu(message)
    except (ObjectDoesNotExist, ValueError):
        text = """Увы, мы не можем найти вас в нашей системе.\nВы уверены, что уже зарегестрированы?"""
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('Да', 'Нет')
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, process_step)


def mainmenu(message):
    text = 'Выберите источник рекомендации:\n✔ Если вы хотите сразу получить подходящую книгу, отправте "Подходящие"\n✔ Если вы хотите получить книгу, пройдя квиз, отправте "Квиз"'
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('Подходящие', 'Квиз')
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, get_book)


def get_book(message):
    if message.text not in ['Подходящие', 'Квиз']:
        bot.send_message(message.chat.id, 'Некорректный ответ')
        mainmenu(message)
        return
    else:
        if message.text == 'Квиз':
            bot.send_message(message.chat.id, 'Выбираем информацию для квиза...')
            bot.send_chat_action(message.chat.id, action='typing')
            reader_id = BotUser.objects.get(tg_id=message.from_user.id).reader.id

            books_with_quotes = []
            books = requests.post('http://46.101.126.232:9871/api/get_preds/',
                                  json={'user_id': reader_id}).json()['books']

            for book in books:
                if book['cover_url'] and len(books_with_quotes)<3:
                    books_with_quotes.append(book['id'])

            if len(books_with_quotes) != 3:
                for i in range(3-len(books_with_quotes)):
                    while True:
                        book_id = Quote.objects.order_by('?').first().book_id
                        if book_id not in books_with_quotes:
                            books_with_quotes.append(book_id)
                            break
            text = "Чтобы мы подобрали для вас интересную книгу, выберите номер наиболее привлекательной цитаты из списка:"
            for num, book in enumerate(books_with_quotes):
                max_rate = Quote.objects.all().filter(book_id=book).aggregate(Max('rating'))['rating__max']
                quote = Quote.objects.filter(book_id=book, rating=max_rate).first().text
                text += f"\n{num+1}. {quote}"

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add('1', '2', '3')
            msg = bot.send_message(message.chat.id, text, reply_markup=markup)
            bot.register_next_step_handler(msg, get_book_by_quote, books_with_quotes)

        else:
            bot.send_message(message.chat.id, 'Подбираем вам книгу...')
            bot.send_chat_action(message.chat.id, action='typing')
            reader_id = BotUser.objects.get(tg_id=message.from_user.id).reader.id

            kniga = None
            while not kniga:
                books = requests.post('http://46.101.126.232:9871/api/get_preds/',
                                      json={'user_id':reader_id}).json()['books']
                while True:
                    book = books[random.randint(0, len(books) - 1)]
                    if book['title'] == 'nan' or not book['title']:
                        continue
                    else:
                        break
                book_id = book['id']
                try:
                    kniga = Catalog.objects.get(id=book_id)
                except ObjectDoesNotExist:
                    print(f"Unknown {book_id}")
                    continue

            text = f"Рекомендую вам к прочтению данную книгу:"
            if kniga.title and kniga.title != 'nan':
                text += f'\n\nНазвание: "{kniga.title}"'
            if kniga.author and kniga.author != 'nan':
                text += f"\n\nАвтор: {kniga.author}"
            if kniga.year and kniga.year != 'nan':
                text += f"\n\nГод выпуска: {kniga.year}"
            if kniga.tags and kniga.tags != 'nan':
                text += f"\n\nТэги: {kniga.tags}"
            text += f"\n\nНадеемся, что она вам понравится!"
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(
                                               'Подобрать ещё одну книгу')
            if not kniga.cover_url:
                msg = bot.send_message(message.chat.id, text, reply_markup=markup)
            else:
                msg = bot.send_photo(message.chat.id, photo=kniga.cover_url, caption=text, reply_markup=markup)

            bot.register_next_step_handler(msg, mainmenu)


def get_book_by_quote(message, data):
    if message.text not in ['1', '2', '3']:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('1', '2', '3')
        msg = bot.send_message(message.chat.id,
                               'Пожалуйста, укажите ответ в качестве номера цитаты.', reply_markup=markup)
        bot.register_next_step_handler(msg, get_book_by_quote, data)
    else:
        book_id = data[int(message.text)-1]
        kniga = Catalog.objects.get(id=book_id)
        text = f"Рекомендую вам к прочтению данную книгу:"
        if kniga.title and kniga.title != 'nan':
            text += f'\n\nНазвание: "{kniga.title}"'
        if kniga.author and kniga.author != 'nan':
            text += f"\n\nАвтор: {kniga.author}"
        if kniga.year and kniga.year != 'nan':
            text += f"\n\nГод выпуска: {kniga.year}"
        if kniga.tags and kniga.tags != 'nan':
            text += f"\n\nТэги: {kniga.tags}"
        text += f"\n\nНадеемся, что она вам понравится!"
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(
            'Подобрать ещё одну книгу')
        if not kniga.cover_url:
            msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        else:
            msg = bot.send_photo(message.chat.id, photo=kniga.cover_url, caption=text, reply_markup=markup)

        bot.register_next_step_handler(msg, mainmenu)


if __name__ == '__main__':
     bot.polling(none_stop=False)
