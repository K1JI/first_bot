import telebot
import random
import os
from random import choice
from telebot import types
from config import ECO

bot = telebot.TeleBot(ECO)

user_dict = {}
class User:
    def __init__(self, name):
        self.name = name

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """\
Привет, я бот по защите нашей планеты
Как мне к тебе обращаться? 
""")
    bot.register_next_step_handler(message, monolog)

def monolog(message):
    try:
        bot.reply_to(message, """\
    Загрязнение окружающей среды: воздух, море и земля
    Окружающая среда всё чаще подвергается негативному влиянию деятельности человека.
    Две наиболее острые экологические проблемы современности — это загрязнение 
    воздуха промышленными выбросами и загрязнение морей мусором, особенно пластиком.
    """)
        bot.register_next_step_handler(message, eco)
    except UnboundLocalError:
        bot.reply_to(message, 'oops')
    
def eco(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Мы должны уменьшить колличество заводов!', 'Сортировать мусор', 'Всё и сразу')
    msg = bot.reply_to(message, 'Что мы должны сделать?', reply_markup=markup)
    




bot.infinity_polling()