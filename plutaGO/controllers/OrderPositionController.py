import sqlite3
from models.Order_position import OrderPosition  # Załóżmy, że istnieje klasa OrderPosition
from .BaseController import BaseController


class OrderPositionController(BaseController):
    def __init__(self, db_path):
        super().__init__(db_path)

    def create(self, order_position: OrderPosition):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                INSERT INTO order_position (order_id, product_id, amount)
                VALUES (?, ?, ?)
                """, (order_position.order_id, order_position.product_id, order_position.amount))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Database error: {e}")

    def get_all(self):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM order_position')
            rows = cursor.fetchall()
            return [OrderPosition(*row) for row in rows]

    def delete(self, order_position_id):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM order_position WHERE id=?", (order_position_id,))
                conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Error deleting order position: {e}")
                return False

    def update(self, order_position_id, new_data):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                UPDATE order_position SET order_id=?, product_id=?, description=?, category_id=?, photo=?, price=?
                WHERE id=?
                """, (new_data['order_id'], new_data['product_id'], new_data['description'], new_data['category_id'], new_data['photo'], new_data['price'], order_position_id))
                conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Error updating order position: {e}")
                return False

    def get_order_position_by_id(self, order_position_id):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM order_position WHERE id=?", (order_position_id,))
            row = cursor.fetchone()
            if row:
                return OrderPosition(*row)
            return None

    def get_order_positions_by_order_id(self, order_id):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM order_position WHERE order_id=?", (order_id, ))
            rows = cursor.fetchall()
            order_positions = [OrderPosition(*order_position) for order_position in rows]
            return order_positions
    
    def delete_by_order_id(self, order_id):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM order_position WHERE order_id = ?", (order_id, ))