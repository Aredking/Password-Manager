from typing import Any

from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex, QAbstractItemModel
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QStyledItemDelegate, QPushButton, QWidget, QStyleOptionViewItem

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
            headers = ["Источник", "Логин", "Пароль", "bnb"]
            return headers[section]
        return None


class PasswordDelegate(QStyledItemDelegate):
    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: 'QModelIndex') -> QWidget:
        button = QPushButton("Показать пароль", parent)
        button.setFixedSize(100, 25)
        return button

    def paint(self, painter: 'QPainter', option: 'QStyleOptionViewItem', index: 'QModelIndex'):
        painter.save()
        painter.drawText(option.rect, Qt.AlignmentFlag.AlignCenter, "⚙")
        painter.restore()

    def setEditorData(self, editor: QWidget, index: 'QModelIndex'):
        # Привязываем логику к кнопке (например, показ пароля)
        password = index.model().data(index, Qt.ItemDataRole.DisplayRole)
        editor.clicked.connect(lambda: print(f"Пароль: {password}"))  # Пример логики

    def setModelData(self, editor: QWidget, model: 'QAbstractItemModel', index: 'QModelIndex'):
        pass
