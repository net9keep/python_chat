#database

import sqlite3

class DataBase:

    def __init__(self):
        self.conn_db = ""
        self.cur = ""

    def connect_db(self):
        self.conn_db = sqlite3.connect("user.db")
        self.find_user()

    def find_user(self):
        with self.conn_db:
            self.cur = self.conn_db.cursor()
            query_message = ""
            self.cur.execut(query_message)
            rows = self.cur.fetchall()
            print(rows)