#database

import sqlite3


class DataBase:

    def __init__(self):
        self.conn_db = ""
        self.cur = ""

    def connect_db(self):
        self.conn_db = sqlite3.connect("user.db")

    def find_user(self, id, pw):
        with self.conn_db:
            self.cur = self.conn_db.cursor()
            if id and pw:
                query_message = "select id, pw from user where id='" + id + "' and pw='" + pw + "'"
            elif id:
                query_message = "select id, pw from user where id='" + id + "'"

            self.cur.execute(query_message)
            rows = self.cur.fetchall()
            return rows

    def login(self, id, pw):
        self.connect_db()
        result = self.find_user(id, pw)
        if result:
            return True
        else:
            return False

    def sign_up(self, id, pw):
        self.connect_db()
        result_id = self.find_user(id, pw="")
        if result_id:
            #TODO write signUp false
            return False
        else:
            #TODO write signUp success
            with self.conn_db:
                self.cur = self.conn_db.cursor()
                query_message = "insert into user (id, pw) values ('" + id + "', '" + pw + "')"
                self.cur.execute(query_message)
            result = self.find_user(id,pw)
            if result:
                return True
            else:
                return False