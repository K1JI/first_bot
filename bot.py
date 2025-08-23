import telebot
import random
from config import TOKEN

bot = telebot.TeleBot(TOKEN)
pass_long = 10
    
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Привет, я тестовый бот")

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
    elif gue_num > num:
        bot.reply_to(message, f"Попытка {atte}: Загадоное число меньше")
    else:
        bot.reply_to(message, f"Попытка {atte}: Загадоное число больше")

    if atte == 6 and num is not None:
        bot.reply_to(message, f"Попытки закончились. Загадоным числом было {num}")
        num = None

@bot.message_handler(func=lambda message: True)
def any_mesage(message):
    print(message)
    bot.send_message(message.chat.id, message.text)

bot.infinity_polling()