import sqlite3
import json


class UserModel:
    def __init__(self, username, password, token, cookie):
        self.username = username
        self.password = password
        self.token = token
        self.cookie = cookie

        self.create_table()

    @staticmethod
    def _connect():
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        return conn, cursor

    @staticmethod
    def _close(conn):
        conn.commit()
        conn.close()

    @classmethod
    def create_table(cls):
        conn, cursor = cls._connect()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                token TEXT,
                cookie TEXT
            )
        ''')
        cls._close(conn)

    def save(self):
        conn, cursor = self._connect()
        cursor.execute('''
            INSERT INTO users (username, password, token, cookie)
            VALUES (?, ?, ?, ?)
        ''', (self.username, self.password, self.token, json.dumps(self.cookie)))
        self._close(conn)

    @classmethod
    def get_all_users(cls):
        conn, cursor = cls._connect()
        cursor.execute('SELECT * FROM users')
        user_data = cursor.fetchall()
        cls._close(conn)
        if user_data:
            return [cls(*data[1:]) for data in user_data]
        return []

    @classmethod
    def get_user_by_username(cls, username):
        conn, cursor = cls._connect()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user_data = cursor.fetchone()
        cls._close(conn)
        if user_data:
            return cls(*user_data[1:])
        return None

    def update(self):
        conn, cursor = self._connect()
        cursor.execute('''
            UPDATE users
            SET password = ?, token = ?, cookie = ?
            WHERE username = ?
        ''', (self.password, self.token, json.dumps(self.cookie), self.username))
        self._close(conn)

    @classmethod
    def delete_all_users(cls):
        conn, cursor = cls._connect()
        cursor.execute('DELETE FROM users')
        cls._close(conn)

    def delete(self):
        conn, cursor = self._connect()
        cursor.execute('DELETE FROM users WHERE username = ?', (self.username,))
        self._close(conn)



# Get all users
# all_users = UserModel.get_all_users()
# for user in all_users:
#     print("Username:", user.username)
#     print("Password:", user.password)
#     print("Token:", user.token)
#     print("Cookie:", user.cookie)
#     print("-----------------")