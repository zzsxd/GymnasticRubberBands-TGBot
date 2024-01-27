#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################

############static variables#####################
TG_api = ''
admins = [818895144, 1897256227]
DB_name = 'users.db'
#################################################

import telebot
import time
from Backend import DB
from Frontend import Bot_inline_btns, User_data

bot = telebot.TeleBot(TG_api)


@bot.message_handler(commands= ['start', 'admin'])
def start(message):

    buttons = Bot_inline_btns()
    command = message.text.replace('/', '')
    user_ID = message.from_user.id
    user.init(user_ID, admins)
    if not user.get_players()[user_ID][1]:
        if command == 'start':
            bot.send_message(message.chat.id, 'Введите номер телефона: ')
            bot.send_message(message.chat.id, 'Привет👋\nСпасибо за покупку резинки для спорта😊\nВ подарок мы хотим отправить вам видео-тренировку🎁\n', reply_markup=buttons.start_btns())
        elif command == 'admin' and user.get_players()[user_ID][0]:
            bot.send_message(message.chat.id, f'Добро пожаловать, {message.from_user.first_name}👋', reply_markup=buttons.admin_btns())

@bot.message_handler(content_types=['text'])
def number(message):

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    buttons = Bot_inline_btns()
    if call.data == 'gift':
        video = open('video.mp4', 'rb')
        bot.send_video(call.message.chat.id, video)

user = User_data()
db = DB(DB_name)
bot.polling(none_stop=True)