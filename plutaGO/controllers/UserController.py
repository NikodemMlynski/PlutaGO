import sqlite3
from models.User import User
class UserController:
    def __init__(self):
        self.conn = sqlite3.connect('plutaGO.db')
        self.cursor = self.conn.cursor()

    def create(self, user: User):
        # Use user object attributes for insertion
        try:
            self.cursor.execute("""
            INSERT INTO users (name, surname, email, password, role)
            VALUES (?, ?, ?, ?, ?)
            """, (user.name, user.surname, user.email, user.password, user.role))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def get_all(self):
        self.cursor.execute('SELECT * FROM users')
        rows = self.cursor.fetchall()
        return [User(*row) for row in rows]

    def delete(self, user_id):
        try:
            self.cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting user: {e}")
            return False

    def update(self, user_id, new_data):
        try:
            self.cursor.execute("UPDATE users SET name=?, surname=?, email=?, password=?, role=? WHERE id=?",
                                (new_data['name'], new_data['surname'], new_data['email'], new_data['password'],
                                 new_data['role'], user_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating user: {e}")
            return False

    def get_user_by_id(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
        row = self.cursor.fetchone()
        if row:
            return User(*row)
        return None


