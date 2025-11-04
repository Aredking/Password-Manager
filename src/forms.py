from PyQt6.QtWidgets import QWidget, QLineEdit, QTableView, QHeaderView
from PyQt6 import uic

from src.database.account_dao import AccountDAO
from src.database.entities import Account
from src.widgets import PasswordsTableModel

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
        uic.loadUi(ui_path, self)

        self.lineEdit: QLineEdit

        self.lineEdit.returnPressed.connect(self.main_window.goto_passwords_manager_form)


class PasswordsManagerForm(ParentForm):
    def __init__(self, main_window):
        super().__init__(main_window)

    def initUI(self):
        base_dir = os.path.dirname(__file__)  # директория, где лежит текущий файл
        ui_path = os.path.join(base_dir, "..", "res", "ui", "passwordsManagerForm.ui")
        uic.loadUi(ui_path, self)

        self.passwordsTable: QTableView
        header = self.passwordsTable.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.load_table()


    def load_table(self):
        dao = AccountDAO()
        self.passwordsTable.setModel(PasswordsTableModel(dao.get_all_accounts()))
