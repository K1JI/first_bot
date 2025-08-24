import telebot
import random
import os
from random import choice
from telebot import types
from config import TOKEN

bot = telebot.TeleBot(TOKEN)
pass_long = 10

user_dict = {}


class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.sex = None


@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Привет, я тестовый бот
Как тебя зовут? 
""")
    bot.register_next_step_handler(message, process_name_step)


def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'Сколько тебе лет?')
        bot.register_next_step_handler(message, process_age_step)
    except Exception as e:
        bot.reply_to(message, 'бип буп ошибка')


def process_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        if not age.isdigit():
            msg = bot.reply_to(message, 'Возраст должен быть в цифрах. Сколько тебе лет?')
            bot.register_next_step_handler(msg, process_age_step)
            return
        user = user_dict[chat_id]
        user.age = age
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Парень', 'Девушка')
        msg = bot.reply_to(message, 'Ты парень или девушка?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_sex_step)
    except Exception as e:
        bot.reply_to(message, 'бип буп ошибка')


def process_sex_step(message):
    try:
        chat_id = message.chat.id
        sex = message.text
        user = user_dict[chat_id]
        if (sex == u'Парень') or (sex == u'Девушка'):
            user.sex = sex
        else:
            raise Exception("Неизвестный пол")
        bot.send_message(chat_id, f"""\
Приятно познакомится {user.name}
Возраст: {user.age}
Пол: {user.sex}
Доступные команды: /guess_num, /password, /heh, /meme'
""")
    except Exception as e:
        bot.reply_to(message, 'бип буп ошибка')

    
@bot.message_handler(commands=['meme'])
def send_meme(message):
    r_meme = choice(os.listdir('images_bot')) 
    with open(f'images_bot/{r_meme}', 'rb') as f:  
        bot.send_photo(message.chat.id, f)  

@bot.message_handler(commands=['heh'])
def send_heh(message):
    count_heh = int(message.text.split()[1]) if len(message.text.split()) > 1 else 5
    bot.reply_to(message, "he" * count_heh)


@bot.message_handler(commands=['password'])
def gen_pass(message):
    chars = "!?+&=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    pas = ""
    for i in range(10):
        pas += random.choice(chars)
    bot.reply_to(message, f'Сгенерированный пароль: {pas}')

num = None 
atte = 0 

@bot.message_handler(commands=['guess_num'])
def start_game(message):
    global num, atte
    num = random.randint(1, 100)
    atte = 0
    bot.reply_to(message, "Было загадано число от 1 до 100. Попробуйте угадать! У тебя 5 попыток")

@bot.message_handler(content_types=['text'])
def guess(message):
    global num, atte
    if num is None: 
        return  

    try:
        gue_num = int(message.text)
    except ValueError:
        bot.reply_to(message, "Введите число!")
        return

    atte += 1
    if gue_num == num:
        bot.reply_to(message, f"Вы угадали! Попыток потрачано: {atte}")
        num = None
    elif gue_num > num and atte < 6:
        bot.reply_to(message, f"Попытка {atte}: Загадоное число меньше")
    elif gue_num < num and atte < 6:
        bot.reply_to(message, f"Попытка {atte}: Загадоное число больше")

    if atte > 5 and num is not None:
        bot.reply_to(message, f"Попытки закончились. Загадоным числом было {num}")
        num = None

@bot.message_handler(func=lambda message: True)
def any_mesage(message):
    print(message)
    bot.send_message(message.chat.id, message.text)

bot.infinity_polling()
