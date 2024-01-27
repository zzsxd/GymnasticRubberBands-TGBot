#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################

import copy

from telebot import types


class Bot_inline_btns:
    def __init__(self):
        super(Bot_inline_btns, self).__init__()
        self.__markup = types.InlineKeyboardMarkup(row_width=1)

    def start_btns(self):
        getvideo = types.InlineKeyboardButton('Получить подарок', callback_data='gift')
        self.__markup.add(getvideo)
        return self.__markup

    def admin_btns(self):
        export_csv = types.InlineKeyboardButton('Экспортировать БД (.csv)', callback_data='export_csv')
        export_xlsx = types.InlineKeyboardButton('Экспортировать БД (.xlsx)', callback_data='export_xlsx')
        self.__markup.add(export_csv, export_xlsx)
        return self.__markup

    def review(self):
        reviewbtn = types.InlineKeyboardButton('Оставить отзыв', url='https://vk.com/feed')
        self.__markup.add(reviewbtn)
        return self.__markup


class User_data:  ### взаимодействие со словарём состояний пользователей
    def __init__(self):
        super(User_data, self).__init__()
        self.__online_users = {}
        self.__default_user = [False]

    def init(self, id):  ### запускается только один раз при вводе /start
        if id not in self.__online_users.keys():
            self.__online_users.update({id: copy.deepcopy(self.__default_user)})

    def get_players(self, user_id):
        return self.__online_users[user_id]