#################################################
#                 created by                    #
#                     ZZS                       #
#                     SBR                       #
#################################################
import csv
import os
import sqlite3


class DB:
    def __init__(self, path):
        super(DB, self).__init__()
        self.__db_path = path
        self.cursor = None
        self.db = None
        self.init()

    def init(self):
        if not os.path.exists(self.__db_path):
            self.db = sqlite3.connect(self.__db_path, check_same_thread=False)
            self.cursor = self.db.cursor()
            self.cursor.execute('''CREATE TABLE users(
                            user_id integer,
                            nick_name text,
                            name text,
                            last_name text,
                            phone text,
                            is_admin text
                            )
                            ''')
            self.db.commit()
        else:
            self.db = sqlite3.connect(self.__db_path, check_same_thread=False)
            self.cursor = self.db.cursor()

    def db_write(self, user_id, nick_name, name, last_name, phone, is_admin):
        self.cursor.execute('INSERT INTO users (?, ?, ?, ?, ?, ?)', (user_id, nick_name, name, last_name, phone, is_admin))
        self.db.commit()

    def db_read(self, user_id, mode):
        self.cursor.execute(f'SELECT ? FROM users WHERE user_id = "{user_id}"')
        self.db.commit()
        for i in self.cursor.fetchall():
            out.append(i)
        if len(out) != 0:
            return out

    def db_export_csv(self):
        self.cursor.execute('SELECT user_id, nick_name, name, last_name, phone FROM users')
        data = self.cursor.fetchall()
        with open('output.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Никнейм', 'Имя', 'Фамилия', 'Номер телефона'])
            writer.writerows(data)

    def quantity_records(self):
        self.cursor.execute('SELECT COUNT(*) FROM users')
        quantity = list(self.cursor.fetchone())
        return quantity[0]
