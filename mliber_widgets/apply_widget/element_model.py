# -*- coding:utf-8 -*-
from Qt.QtCore import QModelIndex, Qt, QAbstractListModel


class ElementModel(QAbstractListModel):
    def __init__(self, model_data=[], parent=None):
        super(ElementModel, self).__init__(parent)
        self.model_data = model_data

    def rowCount(self, parent=QModelIndex()):
        return len(self.model_data)

    def data(self, index, role=Qt.UserRole):
        if not index.isValid():
            return
        row = index.row()
        item = self.model_data[row]
        if role == Qt.UserRole:
            return item

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def insertRows(self, position, count, value, parent=QModelIndex()):
        self.beginInsertRows(parent, position, position+count-1)
        for index, i in enumerate(value):
            self.model_data.insert(position+index, i)
        self.endInsertRows()
        return True

    def removeRows(self, position, count, parent=QModelIndex()):
        self.beginRemoveRows(parent, position, position+count-1)
        for i in range(count):
            value = self.model_data[position]
            self.model_data.remove(value)
        self.endRemoveRows()
        return True

    def setData(self, index, value, role=Qt.UserRole):
        """
        :param index:
        :param value: <list> [type, value]
        :param role:
        :return:
        """
        row = index.row()
        if value:
            if role == Qt.UserRole:
                self.model_data[row] = value
                self.dataChanged.emit(index, index)
            return True

    def remove_all(self):
        for i in xrange(self.rowCount()):
            self.removeRows(0, 1)
