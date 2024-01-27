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
                            name text,
                            username text,
                            phone text
                            )
                            ''')
            self.db.commit()
        else:
            self.db = sqlite3.connect(self.__db_path, check_same_thread=False)
            self.cursor = self.db.cursor()

    def db_write(self, user_id, name, username, phone):
        self.cursor.execute('INSERT INTO users (?, ?, ?, ?)', (user_id, name, username, phone))
        self.db.commit()

    def db_read(self, data, mode):
        out = []
        years = []
        if mode == 'year' and '-' in data:
            years.extend(data.split('-'))
            self.cursor.execute(
                f'SELECT name, year, janre, rate, country, watchtime, desc, link, cover FROM films WHERE {mode} BETWEEN {years[0]} AND {years[1]} order by name')
        else:
            self.cursor.execute(
                f'SELECT name, year, janre, rate, country, watchtime, desc, link, cover FROM films WHERE {mode} LIKE "%{data}%" order by name')
        self.db.commit()
        for i in self.cursor.fetchall():
            out.append(i)
        if len(out) != 0:
            return out

    def db_export_csv(self):
        self.cursor.execute('SELECT user_id, name, username, phone FROM users')
        data = self.cursor.fetchall()
        with open('output.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Column 1', 'Column 2', ...])
            writer.writerows(data)
