import sys

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow, QApplication

from src.ui.entry_form import EntryForm
from src.ui.passwords_manager_form import PasswordsManagerForm


class MainWindow(QMainWindow):
    SIZE = (800, 600)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Manager")
        self.setFixedSize(QSize(*MainWindow.SIZE))

        self.setCentralWidget(EntryForm(self))

    def goto_passwords_manager(self):
        self.centralWidget().deleteLater()
        self.setCentralWidget(PasswordsManagerForm(self))  # Не забываем обновить центральный виджет!

    def goto_passwords_generator(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
