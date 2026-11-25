import telebot 
import requests
import time
from telebot import types
import threading
import os
from google import genai
import google.generativeai as genai

token="8834574509:AAHjdAL7TV7R_BrUB9mIibS5fvT9SOAx3zU"
bot=telebot.TeleBot(token)

norm=2000
user_data = {}


def reminder(chat_id):
    while user_data.get(chat_id, {}).get('active'):
        time.sleep(3600) 
        bot.send_message(chat_id, "ВЫПЕЙ ВОДЫ")

def save(message):
    chat_id=message.chat.id
    try:
       
        sad=int(message.text)
        if chat_id not in user_data:
            user_data[chat_id] = {'drunk': 0, 'active': True}

        user_data[chat_id]['drunk'] += sad
        preresult = norm - user_data[chat_id]['drunk']
        if user_data[chat_id]['drunk'] >= norm:
            bot.send_message(chat_id, "Ты это СДЕЛАЛ!")
            user_data[chat_id]['drunk'] = 0
        else:
            bot.send_message(chat_id, f"Тебе осталось выпить {preresult} мл")

    except ValueError:
        bot.send_message(message.chat.id, "Это не цифры Бро")



@bot.message_handler(commands=["start"])
def start_message(message):
   
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("ДЕРЖАТЬ НОРМУ")
    markup.add(item1)
    bot.send_message(message.chat.id, "Привет, этот бот поможет тебе выполнять суточную нормы воды в день! \n Чтобы начать нажми на кнопку ниже!",reply_markup=markup)

@bot.message_handler(content_types=["text"])
def norm_water(message):
    if message.text=="ДЕРЖАТЬ НОРМУ":
        if not user_data.get(message.chat.id, {}).get('active'):
            user_data[message.chat.id] = {'drunk': 0, 'active': True}
            threading.Thread(target=reminder, args=(message.chat.id,), daemon=True).start()
        else:
            user_data[message.chat.id]['drunk'] = 0
        with open("ВОДЫ.jfif", "rb") as photo:
            bot.send_photo(message.chat.id, photo)
        bot.send_message(message.chat.id, "ВОДЫ")
        markup2=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item2_1=types.KeyboardButton("ВЫПИЛ")
        markup2.add(item2_1)
        bot.send_message(message.chat.id, "Нажимай «ВЫПИЛ», когда попьешь!", reply_markup=markup2)
    elif message.text=="ВЫПИЛ":
                much=bot.send_message(message.chat.id, "Сколько выпил?")
                bot.register_next_step_handler(much, save)

bot.infinity_polling()