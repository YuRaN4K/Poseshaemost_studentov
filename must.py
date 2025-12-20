#shas budet miso
import telebot
from telebot import types
import json
import os

bot = telebot.TeleBot('8485875577:AAEOPEcjP3oTDyMGQKKjOZZyxSjzOcLi7cA')

DATA_FILE = 'dada.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Приветствую!, {message.fron_user.first_name}')
    pupu = types.InlineKeyboardMarkup()
    bat1 = types.InlineKeyboardButton('Расписание', url='https://study.miigaik.ru/group/1510?dateStart=2025-12-15&dateEnd=2025-12-21')
    pupu.row(bat1)
    bat2 = types.InlineKeyboardButton('Данные', callback_data='posechaemosti')
    bat3 = types.InlineKeyboardButton('Уведомить о присутсвии/отсутствии', callback_data='dati vvesti vse dannie')
    pupu.row(bat3, bat2)


@bot.add_callback_query_handler(func=lambda calldack: True)
def callback_massege(callback):
    if callback.data == 'posechaemosti':
        bot.show_all_users(message)
    elif callback.data == 'dati vvesti vse dannie':
        bot.start_form(message)
        def process_form_step(message):
            chat_id = message.chat.id
            step = user_data[chat_id]['step']
    
            if step == 1:
                user_data[chat_id]['name'] = message.text
                user_data[chat_id]['step'] = 2
                bot.send_message(chat_id, 'Имя')
    
            elif step == 2:
                if message.text.isdigit():
                    user_data[chat_id]['prot'] = message.text
                    user_data[chat_id]['step'] = 3
                    bot.send_message(chat_id, 'присутствие/отсутсвие')
            elif step == 3:
                if message.text.isdigit():
                    user_data[chat_id]['pred'] = message.text
                    user_data[chat_id]['step'] = 4
                    bot.send_message(chat_id, 'предмет')
                    user_id = f"user_{chat_id}_{len(data) + 1}"
        
                    data[user_id] = {
                        'telegram_id': chat_id,
                        'telegram_name': call.from_user.username or call.from_user.first_name,
                        'name': user_info['name'],
                        'prot': user_info['prot'],
                        'tpred': user_info['pred'],
                    }
        
                    save_data(data)
        
                    bot.edit_message_text("✅ Данные успешно сохранены!", 
            
bot.polling(none_stop=True)
