#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################

from telebot import types
import copy


class Bot_inline_btns:
    def __init__(self):
        super(Bot_inline_btns, self).__init__()
        self.__markup = types.InlineKeyboardMarkup(row_width=2)

    def start_btns(self):
        getvideo = types.InlineKeyboardButton('Получить подарок', callback_data='gift')
        self.__markup.add(getvideo)
        return self.__markup
class User_data:  ### взаимодействие со словарём состояний пользователей
    def __init__(self):
        super(User_data, self).__init__()
        self.__online_users = {}
        self.__default_admin = [True, False, 0, []]  ### [is_admin, update_db_now, update_index, current_action]

    def init(self, id, admins):  ### запускается только один раз при вводе /start
        default_user = [False, False, 0, [], None]
        if id not in self.__online_users.keys():
            if id in admins:
                default_user[0] = True
            self.__online_users.update({id: copy.deepcopy(default_user)})

    def get_players(self):
        return self.__online_users

    def update_pull(self, tg_id, data):
        self.__online_users[tg_id][3].append(data)

    def update_reset(self, tg_id):
        self.__online_users[tg_id][0:4] = copy.deepcopy(self.__default_admin)