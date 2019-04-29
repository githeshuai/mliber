# -*- coding:utf-8 -*-
from Qt.QtCore import QAbstractTableModel, QModelIndex, Qt


class UserManageModel(QAbstractTableModel):
    def __init__(self, model_data=[], parent=None):
        """
        :param model_data: matrix
        :param parent:
        """
        super(UserManageModel, self).__init__(parent)
        self.__header_list = []
        self.model_data = model_data

    def rowCount(self, parent=QModelIndex()):
        return len(self.model_data)

    def columnCount(self, parent=QModelIndex()):
        if self.model_data:
            return len(self.model_data[0])
        return 0

    def data(self, index, role=Qt.UserRole):
        if not index.isValid():
            return
        row = index.row()
        column = index.column()
        if column in [0, 1, 2, 3, 4, 5, 12]:
            if role == Qt.DisplayRole:
                return self.model_data[row][column]
            if role == Qt.TextAlignmentRole:
                return Qt.AlignCenter
        else:
            if role == Qt.UserRole:
                return self.model_data[row][column]

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def setData(self, index, value, role):
        if not index.isValid():
            return
        if role == Qt.UserRole or role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            if value:
                self.model_data[row][column] = value
                self.dataChanged.emit(index, index)
            return True
        return False

    def insertColumns(self, position, columns, value, parent=QModelIndex()):
        rows = self.rowCount()
        self.beginInsertColumns(parent, position, position+columns-1)
        for row in xrange(rows):
            for index, i in enumerate(value):
                self.model_data[row].insert(position+index, i)
        self.endInsertColumns()
        return True

    def insertRows(self, position, rows, parent=QModelIndex()):
        print "Inserting at row: %s" % position
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            default_data = ["", "", "", "123456", "", "", "False", "False", "False", "True", "True", "Active", ""]
            self.model_data.insert(position+row, default_data)
        self.endInsertRows()
        return True

    def removeColumns(self, position, columns, parent=QModelIndex()):
        rows = self.rowCount()
        self.beginRemoveRows(parent, position, position+columns-1)
        for row in xrange(rows):
            for column in xrange(columns):
                for index, value in enumerate(self.model_data[row]):
                    if index == position:
                        self.model_data[row].remove(value)
        self.endRemoveColumns()
        return True

    def headerData(self, section, orientation, role):
        if self.__header_list and role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.__header_list[section]

    def set_header(self, header_list):
        """
        设置header
        :param header_list:
        :return:
        """
        self.__header_list = header_list
