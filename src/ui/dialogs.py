from PyQt6 import uic
from PyQt6.QtWidgets import (
    QDialog,
    QLineEdit,
    QLabel,
    QMessageBox,
    QInputDialog,
    QPushButton
)
from PyQt6 import QtWidgets

import os

from src.database.dao import UserDAO
from src.database.entities import User, Account
from src.security.password_cipher import check_passwords_hash
from src.security.password_controller import is_password_secure


class NewUserDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        base_dir = os.path.dirname(__file__)
        ui_path = os.path.join(base_dir, "..", "..", "res", "ui",
                               "newUserDialog.ui")  # Здесь я получаю путь к ui файлу.

        self.usernameEdit: QLineEdit = None
        self.passwordEdit: QLineEdit = None
        self.errorLabel: QLabel = None
        uic.loadUi(ui_path, self)

    def accept(self):
        if not self.usernameEdit.text():
            self.errorLabel.setText("Укажите имя пользователя!")
        elif not self.passwordEdit.text():
            self.errorLabel.setText("Укажите пароль!")
        else:
            password_check = is_password_secure(self.passwordEdit.text())
            if UserDAO().user_exists(self.usernameEdit.text()):
                self.errorLabel.setText("Пользователь с таким именем уже существует!")
            elif not password_check[0]:
                self.errorLabel.setText(password_check[1])
            else:
                super().accept()


class AccountDialog(QDialog):
    def __init__(self, account: Account):
        self.account = account

        super().__init__()
        self.initUI()

    def initUI(self):
        base_dir = os.path.dirname(__file__)
        ui_path = os.path.join(base_dir, "..", "..", "res", "ui",
                               "accountDialog.ui")  # Здесь я получаю путь к ui файлу.

        self.sourceEdit: QLineEdit = None
        self.loginEdit: QLineEdit = None
        self.passwordEdit: QLineEdit = None
        self.errorLabel: QLabel = None
        self.okBtn: QPushButton = None
        uic.loadUi(ui_path, self)

        self.okBtn.clicked.connect(self.accept)

        if self.account is None:
            self.setWindowTitle("Новый аккаунт")
        else:
            self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            self.setWindowTitle(self.account.source)
            self.sourceEdit.setText(self.account.source)
            self.loginEdit.setText(self.account.login)
            self.passwordEdit.setText(self.account.password)

    def accept(self):
        if self.account is None:
            if not self.sourceEdit.text():
                self.errorLabel.setText("Укажите источник!")
                return
            elif not self.loginEdit.text():
                self.errorLabel.setText("Укажите логин!")
                return
            elif not self.passwordEdit.text():
                self.errorLabel.setText("Укажите пароль!")
                return

        super().accept()


def show_wrong_password_dialog():
    msg = QMessageBox()
    msg.setWindowTitle("Ввод пароля")
    msg.setText("Неправильный пароль!")
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()


def show_entry_password_dialog(user: User) -> bool | None:
    password, ok = QInputDialog.getText(
        None,
        "Ввод пароля",
        "Введите пароль:",
        echo=QLineEdit.EchoMode.Password
    )
    if not ok:
        return None
    if ok and check_passwords_hash(password.encode(), user.password):
        return True
    return False


def show_user_remove_confirmation_dialog() -> bool:
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Question)
    msg.setWindowTitle("Удаление пользователя")
    msg.setText("Вы действительно хотите удалить аккаунт?")
    msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    msg.setDefaultButton(QMessageBox.StandardButton.No)

    res = msg.exec()
    if res == QMessageBox.StandardButton.Yes:
        return True
    return False
