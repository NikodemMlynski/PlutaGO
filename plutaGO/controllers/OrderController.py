import sqlite3
from models.Order import Order
from .BaseController import BaseController

class OrderController(BaseController):
    def __init__(self, db_path):
        super().__init__(db_path)
    def create(self, order: Order):
        with self.get_db_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                INSERT INTO order (user_id, date, status, address_id)
                VALUES (?, ?, ?, ?)""", (order.user_id, order.date, order.status, order.address_id))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Database error: {e}")

    def get_all(self):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM orders')
            rows = cursor.fetchall()
            return [Order(*row) for row in rows]

    def delete(self, order_id):
        with self.get_db_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM orders WHERE id=?", (order_id,))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error deleting order {e}")

    def update(self, order_id, new_data):
        with self.get_db_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE order SET user_id=?, date=?, status=?, address_id=? WHERE id=?",
                                    (new_data['user_id'], new_data['date'], new_data['status']), new_data['address_id'], order_id)
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error updating order {e}")

    def get_order_by_id(self, order_id):
        with self.get_db_connection() as conn:
            cursor.execute("SELECT * FROM orders where id=?", (order_id,))
            row = cursor.fetchone()
            if row:
                return Order(*row)
            return None