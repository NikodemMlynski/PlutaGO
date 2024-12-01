import sqlite3
from models.Address import Address  # Załóżmy, że istnieje klasa Address
from BaseController import BaseController


class AddressController(BaseController):
    def __init__(self, db_path):
        super().__init__(db_path)

    def create(self, address: Address):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                INSERT INTO addresses (street, city, local_number)
                VALUES (?, ?, ?)
                """, (address.street, address.city, address.local_number))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Database error: {e}")

    def get_all(self):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM addresses')
            rows = cursor.fetchall()
            return [Address(*row) for row in rows]

    def delete(self, address_id):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM addresses WHERE id=?", (address_id,))
                conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Error deleting address: {e}")
                return False

    def update(self, address_id, new_data):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                UPDATE addresses SET street=?, city=?, local_number=? WHERE id=?
                """, (new_data['street'], new_data['city'], new_data['local_number'], address_id))
                conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Error updating address: {e}")
                return False

    def get_address_by_id(self, address_id):
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM addresses WHERE id=?", (address_id,))
            row = cursor.fetchone()
            if row:
                return Address(*row)
            return None