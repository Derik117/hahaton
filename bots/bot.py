# -*- coding: utf-8 -*-
import telebot
from telebot import types
import os
from django.core.exceptions import ObjectDoesNotExist
from hahaton.utils import activate_django_env
activate_django_env()
from data.models.reader import Reader

token = os.environ.get('tg_bot_token')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start", 'help'])
def echo(message):
    text = """
    Добро пожаловать!\nЭтот бот создан для того чтобы посоветовать вам интересную книгу для прочтения.\n\nНо для начала нам нужно познакомиться.\nВы уже зарегестрированы в системе?\nОтвечайте "Да" или "Нет"
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('Да', 'Нет')
    user_id = message.from_user.id
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, process_step)


def process_step(message):
    chat_id = message.chat.id
    if message.text == 'Да':
        msg = bot.send_message(chat_id, 'Отлично, тогда укажите reader_id')
        bot.register_next_step_handler(msg, get_reader_id)
    elif message.text == 'Нет':
        msg = bot.send_message(chat_id, 'Хуёво тебе')
    else:
        msg = bot.send_message(chat_id, 'Отвечай "Да" или "Нет", тварь')
        bot.register_next_step_handler(msg, process_step)


def get_reader_id(message):
    try:
        bot.send_message(message.chat.id, Reader.objects.get(id=message.text).age)
        user_id = message.from_user.id
    except (ObjectDoesNotExist, ValueError):
        text = """Увы, мы не можем найти вас в нашей системе.\nВы уверены, что уже зарегестрированы?"""
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('Да', 'Нет')
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(msg, process_step)


if __name__ == '__main__':
     bot.polling(none_stop=False)
