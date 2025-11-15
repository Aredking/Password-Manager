import sqlite3, os

from src.database.entities import Account, User
from src.security.password_cipher import PasswordsCipher, get_hash_password


class DAO:
    _instance = None

    _FILE_NAME = os.path.join(os.path.dirname(__file__), "..", "..", "database.db")
    _ACCOUNTS_TABLE = "ACCOUNTS"
    _USERS_TABLE = "USERS"

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._create_table()

    def _create_table(self):
        pass


class AccountDAO(DAO):
    def __init__(self):
        super().__init__()

    def _create_table(self) -> None:
        with sqlite3.connect(DAO._FILE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {DAO._ACCOUNTS_TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source VARCHAR(32) NOT NULL,
                login VARCHAR(32) NOT NULL,
                password BLOB NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES USERS (id) ON DELETE CASCADE
            );
            """)

    def get_all_accounts(self, user_id: int) -> list[Account]:
        with sqlite3.connect(DAO._FILE_NAME) as conn:
            cursor = conn.cursor()
            result = cursor.execute(f"""
            SELECT id, source, login, password
            FROM {DAO._ACCOUNTS_TABLE}
            WHERE user_id = ?
            """, (user_id,)).fetchall()

        accounts = list()
        cipher = PasswordsCipher()
        for row in result:
            accounts.append(Account(row[1], row[2], cipher.decode(row[3]), id=row[0]))
        return accounts

    def add_account(self, account: Account, user_id: int) -> None:
        cipher = PasswordsCipher()
        with sqlite3.connect(DAO._FILE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
            INSERT INTO {DAO._ACCOUNTS_TABLE} (source, login, password, user_id) VALUES(?, ?, ?, ?) 
            """, (account.source, account.login, cipher.encode(account.password), user_id))
            conn.commit()

    def delete_by_id(self, account_id: int) -> None:
        with sqlite3.connect(DAO._FILE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
            DELETE FROM {DAO._ACCOUNTS_TABLE} WHERE id = ?
            """, (account_id,))
            conn.commit()

    def update_password(self, account_id: int, new_password: str) -> None:
        with sqlite3.connect(DAO._FILE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
            UPDATE {DAO._ACCOUNTS_TABLE}
            SET password = ?
            WHERE id = ?
            """, (new_password, account_id,))
            conn.commit()


class UserDAO(DAO):
    def __init__(self):
        super().__init__()

    def _create_table(self) -> None:
        with sqlite3.connect(DAO._FILE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS USERS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(32) NOT NULL,
                password BLOB NOT NULL
            );
            """)

    def get_all_users(self) -> list[User]:
        with sqlite3.connect(DAO._FILE_NAME) as conn:
            cursor = conn.cursor()
            result = cursor.execute(f"""
            SELECT * FROM {DAO._USERS_TABLE}
            """).fetchall()

        users = list()
        for row in result:
            users.append(User(row[1], row[2].decode(), id=row[0]))
        return users

    def add_user(self, user: User) -> None:
        with sqlite3.connect(DAO._FILE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
            INSERT INTO {DAO._USERS_TABLE} (username, password) VALUES(?, ?) 
            """, (user.username, get_hash_password(user.password)))
            id = cursor.execute(f"""
            SELECT id FROM {DAO._USERS_TABLE}
            WHERE MAX(id)
            """).fetchone()
            user.id = id[0]
            conn.commit()

    def delete_by_id(self, user_id: int) -> None:
        with sqlite3.connect(DAO._FILE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
            DELETE FROM {DAO._ACCOUNTS_TABLE} WHERE user_id = ?
            """, (user_id,))
            cursor.execute(f"""
            DELETE FROM {DAO._USERS_TABLE} WHERE id = ?
            """, (user_id,))
            conn.commit()

    def update_password(self, user_id: int, new_password: str) -> None:
        with sqlite3.connect(DAO._FILE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
            UPDATE {DAO._USERS_TABLE}
            SET password = ?
            WHERE id = ?
            """, (get_hash_password(new_password), user_id,))
            conn.commit()
