from typing import Any

from PyQt6.QtCore import QAbstractTableModel, Qt

from src.database.entities import Account


class PasswordsTableModel(QAbstractTableModel):
    def __init__(self, data: list[Account]):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return 3

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            account = self._data[index.row()]
            col = index.column()
            if col == 0:
                return account.source
            elif col == 1:
                return account.login
            elif col == 2:
                return account.password

        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole) -> Any:
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            headers = ["Источник", "Логин", "Пароль"]
            return headers[section]
        return None