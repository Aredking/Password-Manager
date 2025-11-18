import sys

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow, QApplication

from src.database.entities import User
from src.ui.forms import EntryForm, PasswordsManagerForm


class MainWindow(QMainWindow):
    __SIZE = (800, 600)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Manager")
        self.setFixedSize(QSize(*MainWindow.__SIZE))

        self.setCentralWidget(EntryForm(self))

    def goto_passwords_manager_form(self, user: User):
        self.centralWidget().deleteLater()
        self.setCentralWidget(PasswordsManagerForm(self, user))  # Не забываем обновить центральный виджет!

    def goto_entry_form(self):
        self.centralWidget().deleteLater()
        self.setCentralWidget(EntryForm(self))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
