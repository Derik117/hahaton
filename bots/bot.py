# -*- coding: utf-8 -*-
import telebot
import os
from hahaton.utils import activate_django_env
activate_django_env()

bot = telebot.TeleBot(os.environ.get('tg_bot_token'))


@bot.message_handler(content_types=["text"])
def echo(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
     bot.polling(none_stop=True)