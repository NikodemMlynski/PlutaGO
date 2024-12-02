import sqlite3

class BaseController:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_db_connection(self):
        return sqlite3.connect(self.db_path)
