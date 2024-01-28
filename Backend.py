#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
import csv
import os
import sqlite3

from pandas import DataFrame


class DB:
    def __init__(self, db_path, dump_path_csv, dump_path_xlsx, lock):
        super(DB, self).__init__()
        self.__db_path = db_path
        self.__dump_path = dump_path_csv
        self.__dump_path_xlsx = dump_path_xlsx
        self.__lock = lock
        self.__fields = ['ID', 'Никнейм', 'Имя', 'Фамилия', 'Номер телефона']
        self.cursor = None
        self.db = None
        self.init()

    def init(self):
        if not os.path.exists(self.__db_path):
            self.db = sqlite3.connect(self.__db_path, check_same_thread=False)
            self.cursor = self.db.cursor()
            self.cursor.execute('''CREATE TABLE users(
                            user_id text,
                            nick_name text,
                            name text,
                            last_name text,
                            phone text,
                            is_admin text,
                            UNIQUE (user_id, nick_name, name, last_name, phone)
                            )
                            ''')
            self.db.commit()
        else:
            self.db = sqlite3.connect(self.__db_path, check_same_thread=False)
            self.cursor = self.db.cursor()

    def db_write(self, user_id, nick_name, name, last_name, phone, is_admin):
        self.set_lock()
        self.cursor.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)', (user_id, nick_name, name, last_name, phone, is_admin))
        self.db.commit()
        self.realise_lock()

    def db_check_exist(self, user_id):
        self.set_lock()
        self.cursor.execute(f'SELECT COUNT(*) FROM users WHERE user_id = "{user_id}"')
        data = self.cursor.fetchone()
        self.realise_lock()
        if data[0] == 1:
            return True

    def db_export_csv(self):
        self.set_lock()
        self.cursor.execute('SELECT user_id, nick_name, name, last_name, phone FROM users')
        data = self.cursor.fetchall()
        self.realise_lock()
        with open(self.__dump_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Никнейм', 'Имя', 'Фамилия', 'Номер телефона'])
            writer.writerows(data)

    def db_export_xlsx(self):
        d = {'ID': [], 'Никнейм': [], 'Имя': [], 'Фамилия': [], 'Номер телефона': []}
        self.set_lock()
        self.cursor.execute('SELECT user_id, nick_name, name, last_name, phone FROM users')
        users = self.cursor.fetchall()
        self.realise_lock()
        for user in users:
            for info in range(len(list(user))):
                d[self.__fields[info]].append(user[info])
        df = DataFrame(d)
        df.to_excel(self.__dump_path_xlsx, sheet_name='пользователи', index=False)

    def quantity_records(self):
        self.set_lock()
        self.cursor.execute('SELECT COUNT(*) FROM users')
        quantity = list(self.cursor.fetchone())
        self.realise_lock()
        return quantity[0]

    def set_lock(self):
        self.__lock.acquire(True)

    def realise_lock(self):
        self.__lock.release()
