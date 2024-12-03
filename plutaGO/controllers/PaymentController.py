import sqlite3
from models.User import User
from .BaseController import BaseController


class PaymentController(BaseController):
    def __init__(self, db_path):
        super().__init__(db_path)

    def create(self, payment):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                INSERT INTO payments (user_id, order_id, price, amount, status, date)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (payment.user_id, payment.order_id, payment.price, payment.amount, payment.status, payment.date))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Database error: {e}")

    def get_all(self):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM payments')
            rows = cursor.fetchall()
            return [payment(*row) for row in rows]

    def delete(self, payment_id):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM payments WHERE id=?", (payment_id,))
                conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Error deleting payment: {e}")
                return False

    def update(self, payment_id, new_data):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                UPDATE payments SET user_id=?, order_id=?, price=?, amount=?, status=?, date=?
                WHERE id=?
                """, (new_data['user_id'], new_data['order_id'], new_data['price'], new_data['amount'], new_data['status'], new_data['date'], payment_id))
                conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Error updating payment: {e}")
                return False

    def get_payment_by_id(self, payment_id):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM payments WHERE id=?", (payment_id,))
            row = cursor.fetchone()
            if row:
                return Payment(*row)
            return None