from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from models.parser import *

class OperationListModel(QAbstractListModel):
    def __init__(self):
        QtCore.QAbstractListModel.__init__(self)
        self.items = []
        
    def data(self, QModelIndex:QModelIndex, role:Qt.DisplayRole) -> str:
        if not QModelIndex.isValid():
            return None
        row = QModelIndex.row()
        if role == QtCore.Qt.DisplayRole:
            name = self.items[row].op.type.value
            return name
        return None

    def rowCount(self, parent=None) -> int:
        return len(self.items)

    def add(self, item:ParsingItem):
        # To notify that the data changes we have to call beginInsertRows and endInsertRows
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.items.append(item)
        self.endInsertRows()
        pass

    def delete(self, index:int):
        # To notify that the data changes we have to call beginInsertRows and endInsertRows
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        if index in range(len(self.items)):
            self.items.pop(index)
        self.endInsertRows()
        pass

    def clear(self):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.items = []
        self.endInsertRows()
        pass
