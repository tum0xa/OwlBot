import requests
import os

import telebot
from telebot.types import Message, Sticker
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
/batch_sticker_start - Начать прием стикеров пачкой
/batch_sticker_end - Вернуть сохраненные стикеры с эмоджи
/help - Вывести это сообщение

Чтобы запросить потверждение чего либо от Совы, просто напишите "Подтверди <ваш текст>". 
Неважно в какой части сообщения и в каком регистре указано слово "Подтверди". 
При любом другом сообщении Сова будет угукать.
Пришлите любой стикер и Сова вернет вам эмоджи и картинку этого стикера.
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


@bot.message_handler(commands=['batch_sticker_start'])
def batch_save_sticker(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Пришлите любое количество стикеров. По окончании наберите команду /batch_sticker_end!')

# Наличие файла  с id чата подразумевает, что была запущена процедура приема стикеров

    f = open(f'{chat_id}.txt', 'w')
    f.writelines('')
    f.close()


@bot.message_handler(commands=['batch_sticker_end'])
def batch_send_sticker(message: Message):
    chat_id = message.chat.id
    if os.path.exists(f'{chat_id}.txt'):
        with open(f'{chat_id}.txt', 'r') as sticker_list: # возращаем пользователю все картинки с эмоджи
            if os.path.getsize(f'{chat_id}.txt') > 0:
                for line in sticker_list.readlines():
                    sticker_file_path, emoji = line.split(',')
                    if os.path.exists(f'{sticker_file_path}'):
                        with open(sticker_file_path, 'rb') as sticker_file:
                            bot.send_message(chat_id, f'{emoji}')
                            bot.send_photo(chat_id, sticker_file)
                        os.remove(f'{sticker_file_path}')
            else:
                bot.send_message(chat_id, 'Вы не прислали ни одного стикера!')
        os.remove(f'{chat_id}.txt')
    else:
        bot.send_message(chat_id, 'Сначала введите команду /batch_sticker_start!')

@bot.message_handler(func=lambda message: True)
def reply_accept(message: Message):
    chat_id = message.chat.id
    if not os.path.exists(f'{chat_id}.txt'):
        if ACCEPT in message.text.lower():
            bot.send_message(chat_id, 'Подтверждаю!')
        else:
            bot.send_message(chat_id, 'Угу')
    else:
        bot.send_message(chat_id, 'Ожидаю стикер или команду /batch_sticker_end')


@bot.message_handler(content_types=['sticker'])
def sticker_to_image(message: Message):
    chat_id = message.chat.id

    if not os.path.exists(f'{chat_id}.txt'): # принимаем по одному стикеры и отдаем картинку с эмоджи
        sticker = save_sticker_to_file(message.sticker, chat_id)
        sticker_file_path = sticker['file_path']
        emoji = sticker['emoji']

        with open(sticker_file_path, 'rb') as sticker_file:
            bot.send_message(chat_id, f'{emoji}')
            bot.send_photo(chat_id, sticker_file)
        os.remove(sticker_file_path)
    else: # принимаем стикеры пачкой
        sticker = save_sticker_to_file(message.sticker, chat_id, batch=True)


def save_sticker_to_file(sticker: Sticker, chat_id, batch = False):
    sticker_str = str(sticker)
    sticker_dict = eval(sticker_str)  # type dict

    file_id = sticker_dict['file_id']
    emoji = sticker_dict['emoji']
    file_info = bot.get_file(file_id)
    file_path_list = file_info.file_path.split('.')
    ext = file_path_list[len(file_path_list) - 1]

    sticker_resp = requests.get(f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}', proxies=proxies)

    file_local_path = '.'.join([file_id, ext])

    with open(file_local_path, 'wb') as sticker_file:
        sticker_file.write(sticker_resp.content)
    if batch:
        with open(f'{chat_id}.txt', 'a') as sticker_list:
            sticker_list.writelines(f'{file_local_path},{emoji}\n')
    sticker_dict = {'file_path': file_local_path, 'emoji': emoji}
    return sticker_dict


bot.polling()
