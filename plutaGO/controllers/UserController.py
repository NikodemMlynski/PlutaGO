import sqlite3
from models.User import User
from .BaseController import BaseController


class UserController(BaseController):
    def __init__(self, db_path):
        super().__init__(db_path)

    def create(self, user: User):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                INSERT INTO users (name, surname, email, password, role, amount_of_pluts)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (user.name, user.surname, user.email, user.password, user.role, user.amount_of_pluts))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Database error: {e}")

    def get_all(self):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users')
            rows = cursor.fetchall()
            return [User(*row) for row in rows]

    def delete(self, user_id):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
                conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Error deleting user: {e}")
                return False

    def update(self, user_id, new_data: User):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("UPDATE users SET name=?, surname=?, email=?, password=?, role=?, amount_of_pluts=? WHERE id=?",
                                (new_data.name, new_data.surname, new_data.email, new_data.password,
                                 new_data.role, new_data.amount_of_pluts, user_id))
                conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Error updating user: {e}")
                return False

    def get_user_by_id(self, user_id):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
            row = cursor.fetchone()
            if row:
                return User(*row)
            return None

    def login(self, email, password):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
            row = cursor.fetchone()
            if row:
                return User(*row)
            else:
                print(f"Invalid email or password")
                return None