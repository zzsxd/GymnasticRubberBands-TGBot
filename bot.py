#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
############static variables#####################
TG_api = '6647107448:AAGTBWiMZZrTgxLoMfOu-8CrSeJqUBkTCeA'
admins = [818895144, 1897256227]
DB_name = 'users.db'
DUMP_name_csv = 'dumps/backup.csv'
DUMP_name_xlsx = 'dumps/backup.xlsx'
#################################################
import telebot
import os
from Backend import DB
from Frontend import Bot_inline_btns, User_data

bot = telebot.TeleBot(TG_api)


@bot.message_handler(commands=['start', 'admin'])
def start(message):
    print('шо хочешь')
    buttons = Bot_inline_btns()
    command = message.text.replace('/', '')
    user_id = message.from_user.id
    is_admin = db.db_read(user_id)
    user_data.init(user_id)
    if is_admin is not None:
        if command == 'start':
            bot.reply_to(message, 'Привет👋\nСпасибо за покупку резинки для спорта😊\nВ подарок мы хотим отправить вам видео-тренировку🎁\n', reply_markup=buttons.start_btns())
            bot.send_message(message.chat.id, 'Оставьте пожалуйста отзыв!', reply_markup=buttons.review())
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
        bot.reply_to(message, 'Привет👋\nСпасибо за покупку резинки для спорта😊\nВ подарок мы хотим отправить вам видео-тренировку🎁\n', reply_markup=buttons.start_btns())
        bot.send_message(message.chat.id, 'Оставьте пожалуйста отзыв!', reply_markup=buttons.review())
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


user_data = User_data()
db = DB(DB_name, DUMP_name_csv, DUMP_name_xlsx)
bot.polling(none_stop=True)
