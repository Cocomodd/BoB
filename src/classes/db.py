import sqlite3
from config import config


class DB:
    def __init__(self):
        self.conn = sqlite3.connect(config.db_name + '.db')

    def get_cursor(self):
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()


db = DB()
