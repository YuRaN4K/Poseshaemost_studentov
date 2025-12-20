#shas budet miso
import telebot
from telebot import types
import json
import os

bot = telebot.TeleBot('8485875577:AAEOPEcjP3oTDyMGQKKjOZZyxSjzOcLi7cA')


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Приветствую!, {message.fron_user.first_name}')
    pupu = types.InlineKeyboardMarkup()
    bat1 = types.InlineKeyboardButton('Расписание', url='https://study.miigaik.ru/group/1510?dateStart=2025-12-15&dateEnd=2025-12-21')
    pupu.row(bat1)
    bat2 = types.InlineKeyboardButton('Данные', callback_data='posechaemosti')
    pupu.row(bat2)


@bot.add_callback_query_handler(func=lambda calldack: True)
def callback_massege(callback):
    if callback.data == 'posechaemosti':
        bot.send_document_command(callback_massege)
        docs = ('...','rb')
        bot.send_document(callback_massege.chat.id, docs, caption="посещаемость")
      
            
bot.infinity_polling(none_stop=True)