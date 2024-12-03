import sqlite3
from models.Category import Category  # Załóżmy, że istnieje klasa Category
from .BaseController import BaseController


class CategoryController(BaseController):
    def __init__(self, db_path):
        super().__init__(db_path)
 
    def create(self, category: Category):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                INSERT INTO categories (name)
                VALUES (?)
                """, (category.name,))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Database error: {e}")

    def get_all(self):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM categories')
            rows = cursor.fetchall()
            return [Category(*row) for row in rows]

    def delete(self, category_id):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM categories WHERE id=?", (category_id,))
                conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Error deleting category: {e}")
                return False

    def update(self, category_id, new_data):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("UPDATE categories SET name=? WHERE id=?",
                                (new_data['name'], category_id))
                conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Error updating category: {e}")
                return False

    def get_category_by_id(self, category_id):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM categories WHERE id=?", (category_id,))
            row = cursor.fetchone()
            if row:
                return Category(*row)
            return None