from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton, QListView, QInputDialog, QMessageBox, QDialog, QTableView, \
    QLabel, QHeaderView
from PyQt6 import uic

from src.database.dao import AccountDAO, UserDAO

import os

from src.database.entities import User, Account
from src.security.password_cipher import check_passwords_hash
from src.security.password_controller import is_password_secure
from src.widgets import UserListModel, AccountsTableModel


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

        self.newUserBtn: QPushButton = None
        self.listUsers: QListView = None

        uic.loadUi(ui_path, self)

        self.newUserBtn.clicked.connect(self.show_add_user_dialog)

        self.load_users()
        self.listUsers.clicked.connect(self.on_user_clicked)

    def load_users(self):
        user_dao = UserDAO()
        self.model = UserListModel(user_dao.get_all_users())
        self.listUsers.setModel(self.model)

    def on_user_clicked(self, index):
        user = index.data(Qt.ItemDataRole.UserRole)
        result_dialog = self.show_entry_password_dialog(user)
        if result_dialog:
            self.main_window.goto_passwords_manager_form(user)
        elif result_dialog is not None:
            self.show_wrong_password_message()

    def show_entry_password_dialog(self, user) -> bool:
        password, ok = QInputDialog.getText(
            None,
            "Ввод пароля",
            "Введите пароль:",
            echo=QLineEdit.EchoMode.Password
        )
        if not ok:
            return
        if ok and check_passwords_hash(password.encode(), user.password):
            return True
        return False

    def show_wrong_password_message(self):
        msg = QMessageBox()
        msg.setWindowTitle("Ввод пароля")
        msg.setText("Неправильный пароль!")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def show_add_user_dialog(self):
        dialog = NewUserDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            user_dao = UserDAO()
            user = User(dialog.usernameEdit.text(), dialog.passwordEdit.text())
            user_dao.add_user(user)
            self.model.add_user(user)
            self.main_window.goto_passwords_manager_form(user)


class PasswordsManagerForm(ParentForm):
    def __init__(self, main_window, user: User):
        self.user = user

        super().__init__(main_window)

    def initUI(self):
        base_dir = os.path.dirname(__file__)
        ui_path = os.path.join(base_dir, "..", "res", "ui",
                               "passwordsManagerForm.ui")  # Здесь я получаю путь к ui файлу.

        self.accountsTable: QTableView = None
        self.newAccountBtn: QPushButton = None

        uic.loadUi(ui_path, self)

        self.accountsTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.accountsTable.setSelectionMode(self.accountsTable.SelectionMode.NoSelection)

        self.__load_table()

        self.newAccountBtn.clicked.connect(self.show_add_account_dialog)

    def __load_table(self):
        dao = AccountDAO()
        self.model = AccountsTableModel(dao.get_all_accounts(self.user.id))
        self.accountsTable.setModel(self.model)

    def show_add_account_dialog(self):
        dialog = NewAccountDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            account_dao = AccountDAO()
            account = Account(dialog.sourceEdit.text(), dialog.loginEdit.text(), dialog.passwordEdit.text())
            account_dao.add_account(
                account, self.user.id)
            self.model.insertRow(account)


class NewUserDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        base_dir = os.path.dirname(__file__)
        ui_path = os.path.join(base_dir, "..", "res", "ui",
                               "newUserDialog.ui")  # Здесь я получаю путь к ui файлу.

        self.usernameEdit: QLineEdit = None
        self.passwordEdit: QLineEdit = None
        self.errorLabel: QLabel = None
        uic.loadUi(ui_path, self)

    def accept(self):
        password_check = is_password_secure(self.passwordEdit.text())
        if not password_check[0]:
            self.errorLabel.setText(password_check[1])
        else:
            super().accept()


class NewAccountDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        base_dir = os.path.dirname(__file__)
        ui_path = os.path.join(base_dir, "..", "res", "ui",
                               "newAccountDialog.ui")  # Здесь я получаю путь к ui файлу.

        self.sourceEdit: QLineEdit = None
        self.loginEdit: QLineEdit = None
        self.passwordEdit: QLineEdit = None
        self.errorLabel: QLabel = None
        uic.loadUi(ui_path, self)

    def accept(self):
        password_check = is_password_secure(self.passwordEdit.text())
        if not password_check[0]:
            self.errorLabel.setText(password_check[1])
        elif not self.sourceEdit.text():
            self.errorLabel.setText("Укажите источник")
        elif not self.loginEdit.text():
            self.errorLabel.setText("Укажите логин")
        else:
            super().accept()

class ShowPasswordDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        base_dir = os.path.dirname(__file__)
        ui_path = os.path.join(base_dir, "..", "res", "ui",
                               "newAccountDialog.ui")  # Здесь я получаю путь к ui файлу.

        self.sourceEdit: QLineEdit = None
        self.loginEdit: QLineEdit = None
        self.passwordEdit: QLineEdit = None
        self.errorLabel: QLabel = None
        uic.loadUi(ui_path, self)


