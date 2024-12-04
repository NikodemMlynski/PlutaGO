from models.Product import  Product
import sqlite3
from .BaseController import BaseController

class ProductController(BaseController):
    def __init__(self, db_path):
        super().__init__(db_path)

    def create(self, product: Product):
        with self.get_db_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                INSERT INTO products (name, description, category_id, photo, price)
                VALUES (?, ?, ?, ?, ?)""", (product.name, product.description, product.category_id, product.photo, product.price))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Database error: {e}")

    def get_all(self):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products")
            rows = cursor.fetchall()
            return [Product(*row) for row in rows]

    def delete(self, product_id):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM products WHERE id=?", (product_id, ))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error deleting product: {e}")

    def update(self, product_id, new_data: Product):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("UPDATE products SET name=?, description=?, category_id=?, photo=?, price=? WHERE id=?",
                               (new_data.name, new_data.description, new_data.category_id, new_data.photo, new_data.price, product_id))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error updating user: {e}")

    def get_product_by_id(self, product_id):
        with self.get_db_connection() as conn:
            cursor = conn.cusror()
            cursor.execute("SELECT * FROM products WHERE id=?", (product_id, ))
            row = cursor.fetchone()
            if row:
                return Product(*row)
            return None