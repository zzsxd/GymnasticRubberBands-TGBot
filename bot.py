#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
############static variables#####################
TG_api = ''
admins = [818895144, 1897256227]
delay = 30 ### min
schedules = []
DB_name = 'users.db'
DUMP_name_csv = 'backup.csv'
DUMP_name_xlsx = 'backup.xlsx'
#################################################

import os
import time
from threading import Thread

import telebot

from Backend import DB
from Frontend import Bot_inline_btns, User_data

bot = telebot.TeleBot(TG_api)


@bot.message_handler(commands=['start', 'admin'])
def start(message):
    buttons = Bot_inline_btns()
    command = message.text.replace('/', '')
    user_id = message.from_user.id
    is_admin = db.db_read(user_id)
    user_data.init(user_id)
    if is_admin is not None:
        if command == 'start':
            start_msg(message, buttons)
        elif command == 'admin' and is_admin[0]:
            bot.reply_to(message, f'Добро пожаловать, {message.from_user.first_name}👋\nВсего пользователей: {db.quantity_records()}', reply_markup=buttons.admin_btns())
    else:
        bot.send_message(message.chat.id, 'Введите номер телефона: ')
        user_data.get_players(user_id)[0] = True


@bot.message_handler(content_types=['text'])
def number(message):
    buttons = Bot_inline_btns()
    user_id = message.from_user.id
    if user_data.get_players(user_id)[0]:
        is_admin = False
        if user_id in admins:
            is_admin = True
        db.db_write(user_id, message.from_user.username, message.from_user.first_name, message.from_user.last_name, message.text, is_admin)
        start_msg(message, buttons)
        user_data.get_players(user_id)[0] = False


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'gift':
        bot.send_video(call.message.chat.id, open('video.mp4', 'rb'))
    elif call.data == 'export_csv':
        db.db_export_csv()
        bot.send_document(call.message.chat.id, open(DUMP_name_csv, 'rb'))
        os.remove(DUMP_name_csv)
    elif call.data == 'export_xlsx':
        db.db_export_xlsx()
        bot.send_document(call.message.chat.id, open(DUMP_name_xlsx, 'rb'))
        os.remove(DUMP_name_xlsx)


def start_msg(message, buttons):
    bot.reply_to(message,
                 'Привет👋\nСпасибо за покупку резинки для спорта😊\nВ подарок мы хотим отправить вам видео-тренировку🎁\n',
                 reply_markup=buttons.start_btns())
    schedules.append([message.chat.id, int(time.time())])


def schedule():
    while True:
        for i in range(len(schedules)):
            if schedules[i][1] + delay*60 <= int(time.time()):
                buttons = Bot_inline_btns()
                bot.send_message(schedules[i][0], 'Оставьте пожалуйста отзыв!', reply_markup=buttons.review())
                del schedules[i]
        time.sleep(1)

user_data = User_data()
db = DB(DB_name, DUMP_name_csv, DUMP_name_xlsx)
Thread(target=schedule).start()
bot.polling(none_stop=True)
