import telebot
from telebot.types import Message
from telebot import apihelper


PROXY = 'https://user:password@80.154.109.12:54219'
TOKEN = '698617737:AAGBqrx8VlE7aMa7KWQGBZdfPWHuKUrCDw!M'
ACCEPT = 'подтверди'
JOKE = '''
Царь позвал к себе Иванушку-дурака и говорит:
– Если завтра не принесешь двух говорящих птиц – голову срублю.
Иван принес филина и воробья. Царь говорит:
– Ну, пусть что-нибудь скажут.
Иван спрашивает:
– Воробей, почем раньше водка в магазине была?
Воробей:
– Чирик.
Иван филину:
– А ты, филин, подтверди.
Филин:
– Подтверждаю.
'''
apihelper.proxy = {'https': PROXY}

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f'Добро пожаловать, {message.from_user.username}')


@bot.message_handler(commands=['joke'])
def send_welcome(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, JOKE)


@bot.message_handler(commands=['sleep'])
def send_welcome(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Спокойной ночи! Угу.")


@bot.message_handler(func=lambda message: True)
def reply_accept(message: Message):
    chat_id = message.chat.id
    if ACCEPT in message.text.lower():
        bot.send_message(chat_id, 'Подтверждаю!')
    else:
        bot.send_message(chat_id, 'Угу')


bot.polling()
