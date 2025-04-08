from flask_login import UserMixin
from.db import get_db_connection

class User(UserMixin):
    def __init__(sel, user_id, username, email, password_hash):
        self.id = user_id
        self.username = username
        self.email = email
        self.password_hash =password_hash

        @staticmethod
        def get(user_id):
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("SELECT user_id, username, email, password_hash FROM users WHERE user_id = %s", (email,))
            user_data = c.fetchone()
            conn.close()
            if user_data:
                return User(user_data[0], user_data[1], user_data[2], user_data[3])
            return None
        

        @staticmethod
        def find_by_email(email):
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("SELECT user_id, username, email, password_hash FROM users WHERE email = %s", (email,))
            user_data = c.fetchone()
            conn.close()
            if user_data:
                return User(user_data[0], user_data[1], user_data[2], user_data[3])
            return None