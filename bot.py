#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
############static variables#####################
TG_api = ''
admins = [737360251, 1897256227, 818895144]
delay = 30 ### min
schedules = []
work_directory = '/root/tg-bot/GymnasticRubberBands-TGBot/' ### '/root/tg-bot/GymnasticRubberBands-TGBot/'
DB_name = work_directory + 'users.db'
DUMP_name_csv = work_directory + 'backup.csv'
DUMP_name_xlsx = work_directory + 'backup.xlsx'
video = work_directory + 'video.mp4'
#################################################

import os
import time
from threading import Lock, Timer

import telebot

from Backend import DB
from Frontend import Bot_inline_btns, User_data

bot = telebot.TeleBot(TG_api)


@bot.message_handler(commands=['start', 'admin'])
def start(message):
    user_id = message.from_user.id
    is_existed = db.db_check_exist(user_id)
    user_data.init(user_id)
    if is_existed:
        buttons = Bot_inline_btns()
        command = message.text.replace('/', '')
        if command == 'start':
            start_msg(message, buttons)
        elif command == 'admin' and user_id in admins:
            bot.reply_to(message, f'Добро пожаловать, {message.from_user.first_name}👋\nВсего пользователей: {db.quantity_records()}', reply_markup=buttons.admin_btns())
    else:
        bot.send_message(message.chat.id, 'Введите номер телефона: ')
        user_data.get_players(user_id)[0] = True


@bot.message_handler(content_types=['text'])
def number(message):
    user_id = message.from_user.id
    user_stat = user_data.get_players(user_id)
    if user_stat is not None:
        buttons = Bot_inline_btns()
        if user_stat[0]:
            is_admin = 'Нет'
            if user_id in admins:
                is_admin = 'Да'
            db.db_write(user_id, message.from_user.username, message.from_user.first_name, message.from_user.last_name,
                        message.text, is_admin)
            start_msg(message, buttons)
            user_stat[0] = False
    else:
        bot.send_message(message.chat.id, 'Введите /start')


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    user_id = call.from_user.id
    user_stat = user_data.get_players(user_id)
    if user_stat is not None:
        buttons = Bot_inline_btns()
        if call.data == 'gift':
            if user_stat[1] + 60 <= int(time.time()):
                bot.send_video(call.message.chat.id, open(video, 'rb'))
                Timer(delay*60, vote_us, args=(call.message.chat.id, buttons)).start()
                user_stat[1] = int(time.time())
            else:
                bot.send_message(call.message.chat.id, 'Подождите 1 минуту!')
        elif call.data == 'export_csv':
            db.db_export_csv()
            bot.send_document(call.message.chat.id, open(DUMP_name_csv, 'rb'))
            os.remove(DUMP_name_csv)
        elif call.data == 'export_xlsx':
            db.db_export_xlsx()
            bot.send_document(call.message.chat.id, open(DUMP_name_xlsx, 'rb'))
            os.remove(DUMP_name_xlsx)
    else:
        bot.send_message(call.message.chat.id, 'Введите /start')


def start_msg(message, buttons):
    bot.reply_to(message,
                 'Привет👋\nСпасибо за покупку резинки для спорта😊\nВ подарок мы хотим отправить вам видео-тренировку🎁\n',
                 reply_markup=buttons.start_btns())


def vote_us(message, buttons):
    bot.send_message(message, 'Оставьте пожалуйста отзыв!', reply_markup=buttons.review())


user_data = User_data()
db = DB(DB_name, DUMP_name_csv, DUMP_name_xlsx, Lock())
bot.polling(none_stop=True)
