import requests

import telebot
from telebot.types import Message
from telebot import apihelper


PROXY = 'https://user:password@54.36.109.28:3128'

TOKEN = '698617737:AAGBqrx8VlE7aMa7KWQGBZdfPWHuKUrCDwM'
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

HELP_TEXT = '''
Доступные команды:
/joke - Рассказать анекдот
/start - Приветствие
/sleep - Сказать спокойной ночи
/help - Вывести это сообщение

Чтобы запросить потверждение чего либо от Совы, просто напишите "Подтверди <ваш текст>". 
Неважно в какой части сообщения и в каком регистре указано слово "Подтверди". 
При любом другом сообщении Сова будет угукать.
'''

apihelper.proxy = {'https': PROXY}
proxies = apihelper.proxy
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


@bot.message_handler(commands=['help'])
def send_welcome(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, HELP_TEXT)


@bot.message_handler(func=lambda message: True)
def reply_accept(message: Message):
    chat_id = message.chat.id
    if ACCEPT in message.text.lower():
        bot.send_message(chat_id, 'Подтверждаю!')
    else:
        bot.send_message(chat_id, 'Угу')


@bot.message_handler(content_types=['sticker'])
def save_sticker(message: Message):

    chat_id = message.chat.id

    sticker_str = str(message.sticker)
    sticker = eval(sticker_str)  # type dict

    file_id = sticker['file_id']
    emoji = sticker['emoji']
    file_info = bot.get_file(file_id)
    file_path_list = file_info.file_path.split('.')
    ext = file_path_list[len(file_path_list)-1]

    sticker_resp = requests.get(f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}', proxies=proxies)

    with open('.'.join([file_id, ext]), 'wb') as sticker_file:
        sticker_file.write(sticker_resp.content)

    with open('.'.join([file_id, ext]), 'rb') as sticker_file:
        bot.send_message(chat_id, f'{emoji}')
        bot.send_photo(chat_id, sticker_file)






bot.polling()
