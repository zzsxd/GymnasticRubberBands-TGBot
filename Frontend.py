#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################

from telebot import types


class Bot_inline_btns:
    def __init__(self):
        super(Bot_inline_btns, self).__init__()
        self.__markup = types.InlineKeyboardMarkup(row_width=2)

    def start_btns(self):
        getvideo = types.InlineKeyboardButton('Получить подарок', callback_data='gift')
        self.__markup.add(getvideo)
        return self.__markup