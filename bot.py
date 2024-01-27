#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################

############static variables#####################
TG_api = ''
#################################################

import telebot

from Frontend import Bot_inline_btns

bot = telebot.TeleBot(TG_api)


@bot.message_handler(commands= ['start', 'admin'])
def start(message):
    buttons = Bot_inline_btns()
    command = message.text.replace('/', '')
    if command == 'start':
        bot.send_message(message.chat.id, 'Привет👋\nСпасибо за покупку резинки для спорта😊\nВ подарок мы хотим отправить вам видео-тренировку🎁\n', reply_markup=buttons.start_btns())



@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    buttons = Bot_inline_btns()
    if call.data == 'gift':
        video_main = open('video_main.mp4', 'rb')
        video = open('video.mp4', 'rb')
        bot.send_video(call.message.chat.id, video_main)
        bot.send_video(call.message.chat.id, video)



bot.polling(none_stop=True)