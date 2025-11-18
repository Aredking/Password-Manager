from PyQt6.QtCore import QAbstractListModel, QModelIndex, Qt, QAbstractTableModel, QSortFilterProxyModel

from src.database.entities import User, Account


class UserListModel(QAbstractListModel):
    def __init__(self, users: list[User] = None):
        super().__init__()
        self._users = users or []

    def rowCount(self, parent=QModelIndex()):
        return len(self._users)

    def data(self, index, role=...):
        if not index.isValid():
            return None

        user = self._users[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            return user.username
        if role == Qt.ItemDataRole.UserRole:
            return user

        return None

    def add_user(self, user: User):
        row = self.rowCount()
        self.beginInsertRows(QModelIndex(), row, row)
        self._users.append(user)
        self.endInsertRows()


class AccountsTableModel(QAbstractTableModel):
    def __init__(self, accounts: list[Account]):
        super().__init__()
        self._accounts = accounts

    def rowCount(self, parent=None):
        return len(self._accounts)

    def columnCount(self, parent=None):
        return 2

    def data(self, index, role=...):
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                return self._accounts[index.row()].source
            if index.column() == 1:
                return self._accounts[index.row()].login

        if role == Qt.ItemDataRole.UserRole:
            return self._accounts[index.row()]

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == Qt.Orientation.Horizontal:
            if section == 0:
                return "Источник"
            if section == 1:
                return "Логин"

        return super().headerData(section, orientation, role)

    def insertRow(self, account: Account, parent=QModelIndex()):
        row = self.rowCount()
        self.beginInsertRows(parent, row, row)
        self._accounts.append(account)
        self.endInsertRows()

    def removeRow(self, row, parent=QModelIndex()):
        if row < 0 or row >= self.rowCount():
            return False

        self.beginRemoveRows(parent, row, row)
        self._accounts.pop(row)
        self.endRemoveRows()
        return True

    def set_accounts(self, accounts):
        self.beginResetModel()
        self._accounts = accounts
        self.endResetModel()
