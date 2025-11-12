from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QLineEdit, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView
from PyQt6 import uic

from src.database.dao import AccountDAO
from src.database.entities import Account

import os


class ParentForm(QWidget):
    def __init__(self, main_window):
        from src.main import MainWindow
        super().__init__()
        self.main_window: MainWindow = main_window
        self.initUI()

    def initUI(self):
        pass


class EntryForm(ParentForm):
    def __init__(self, main_window):
        super().__init__(main_window)

    def initUI(self):
        base_dir = os.path.dirname(__file__)  # директория, где лежит текущий файл
        ui_path = os.path.join(base_dir, "..", "res", "ui", "entryForm.ui")

        self.lineEdit: QLineEdit = None
        uic.loadUi(ui_path, self)

        self.lineEdit.returnPressed.connect(self.main_window.goto_passwords_manager_form)


class PasswordsManagerForm(ParentForm):
    def __init__(self, main_window):
        super().__init__(main_window)

    def initUI(self):
        base_dir = os.path.dirname(__file__)
        ui_path = os.path.join(base_dir, "..", "res", "ui",
                               "passwordsManagerForm.ui")  # Здесь я получаю путь к ui файлу.

        self.passwordsTable: QTableWidget = None
        uic.loadUi(ui_path, self)

        self.passwordsTable.setColumnCount(3)
        self.passwordsTable.setHorizontalHeaderLabels(["Источник", "Логин", "Удалить аккаунт"])
        self.passwordsTable.horizontalHeader().setSelectionMode(self.passwordsTable.SelectionMode.NoSelection)
        self.passwordsTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.passwordsTable.setStyleSheet("""
        QTableWidget {
            font-size: 12pt;
        }
        QHeaderView::section {
            font-size: 12pt;
            font-weight: bold;
        }""")

        self.__load_table()

    def __load_table(self):
        dao = AccountDAO()
        data = dao.get_all_accounts()

        self.passwordsTable.setRowCount(len(data))
        for row, account in enumerate(data):
            self.passwordsTable.setItem(row, 0, QTableWidgetItem(account.source))
            self.passwordsTable.setItem(row, 1, QTableWidgetItem(account.login))
            btn = QPushButton("🗑")
            btn.clicked.connect(lambda r=row: self.__delete_row(r, account.id))
            # btn.setFixedSize(QSize(40, 40))
            self.passwordsTable.setCellWidget(row, 2, btn)

    def __delete_row(self, row, account_id):
        self.passwordsTable.removeRow(row)
