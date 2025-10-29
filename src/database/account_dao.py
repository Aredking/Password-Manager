import sqlite3
from entity import Account


class AccountDAO:
    _instance = None

    __TABLE_NAME = "ACCOUNTS"
    __FILE_NAME = "../../database/database.db"

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self.__is_created_table():
            self.__create_table()
        else:
            print("base already created!")

    def __is_created_table(self) -> bool:
        with sqlite3.connect(AccountDAO.__FILE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name=?
                """, (AccountDAO.__TABLE_NAME,))
            return cursor.fetchone() is not None

    def __create_table(self) -> None:
        with sqlite3.connect(AccountDAO.__FILE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                    CREATE TABLE {AccountDAO.__TABLE_NAME}
                (
                	id INTEGER PRIMARY KEY AUTOINCREMENT,
                	source VARCHAR(32)  NOT NULL,
                	login VARCHAR(32)  NOT NULL,
                	password VARCHAR(32)  NOT NULL
                );
                """)

    def get_all_accounts(self) -> list[Account]:
        with sqlite3.connect(AccountDAO.__FILE_NAME) as conn:
            cursor = conn.cursor()
            result = cursor.execute(f"""
            SELECT * FROM {AccountDAO.__TABLE_NAME}
            """).fetchall()

        accounts = list()
        for row in result:
            accounts.append(Account(row[1], row[2], row[3], id=row[0]))
        return accounts

    def add_account(self, account: Account) -> None:
        with sqlite3.connect(AccountDAO.__FILE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
            INSERT INTO {AccountDAO.__TABLE_NAME} (source, login, password) VALUES(?, ?, ?) 
            """, (account.source, account.login, account.password))
            conn.commit()

    def delete_by_id(self, account_id: int) -> None:
        with sqlite3.connect(AccountDAO.__FILE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
            DELETE FROM {AccountDAO.__TABLE_NAME} WHERE id = ?
            """, (account_id,))
            conn.commit()
