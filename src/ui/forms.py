from PyQt6.QtWidgets import QWidget, QPushButton, QListView, QTableView, QHeaderView

from src.database.dao import AccountDAO, UserDAO

from src.ui.dialogs import *
from src.ui.widgets import *


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
        ui_path = os.path.join(base_dir, "..", "..", "res", "ui", "entryForm.ui")

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
        result_dialog = show_entry_password_dialog(user)
        if result_dialog:
            self.main_window.goto_passwords_manager_form(user)
        elif result_dialog is not None:
            show_wrong_password_dialog()

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
        ui_path = os.path.join(base_dir, "..", "..", "res", "ui",
                               "passwordsManagerForm.ui")  # Здесь я получаю путь к ui файлу.

        self.accountsTable: QTableView = None
        self.newAccountBtn: QPushButton = None
        self.removeAccountBtn: QPushButton = None
        self.returnBtn: QPushButton = None
        self.removeUser: QPushButton = None

        uic.loadUi(ui_path, self)

        self.accountsTable.doubleClicked.connect(self.on_cell_double_clicked)
        self.accountsTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.accountsTable.setSelectionMode(self.accountsTable.SelectionMode.NoSelection)

        self.__load_table()

        self.newAccountBtn.clicked.connect(lambda: self.show_account_dialog(None))
        self.removeAccountBtn.clicked.connect(self.remove_account)
        self.returnBtn.clicked.connect(self.main_window.goto_entry_form)
        self.removeUser.clicked.connect(self.remove_user)

    def __load_table(self):
        dao = AccountDAO()
        self.model = AccountsTableModel(dao.get_all_accounts(self.user.id))
        self.accountsTable.setModel(self.model)

    def on_cell_double_clicked(self, index):
        if index.isValid():
            data = self.model.data(index, Qt.ItemDataRole.UserRole)
            self.show_account_dialog(data)

    def show_account_dialog(self, account: Account):
        account_dao = AccountDAO()
        dialog = AccountDialog(account)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            if account is not None:
                if dialog.sourceEdit.text() != dialog.account.source or dialog.loginEdit.text() != dialog.account.login or dialog.passwordEdit.text() != dialog.account.password:
                    account_dao.update_account(account.id, Account(dialog.sourceEdit.text(), dialog.loginEdit.text(),
                                                                   dialog.passwordEdit.text()))
                    self.model.set_accounts(account_dao.get_all_accounts(self.user.id))
            else:
                account = Account(dialog.sourceEdit.text(), dialog.loginEdit.text(), dialog.passwordEdit.text())
                account_dao.add_account(
                    account, self.user.id)
                self.model.insertRow(account)

    def remove_account(self):
        if self.accountsTable.currentIndex().isValid():
            data = self.model.data(self.accountsTable.currentIndex(), Qt.ItemDataRole.UserRole)
            AccountDAO().delete_by_id(data.id)
            self.model.removeRow(self.accountsTable.currentIndex().row())

    def remove_user(self):
        if show_user_remove_confirmation_dialog():
            user_dao = UserDAO()
            user_dao.delete_by_id(self.user.id)
            self.main_window.goto_entry_form()
