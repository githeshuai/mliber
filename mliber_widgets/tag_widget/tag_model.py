# -*- coding:utf-8 -*-
from Qt.QtGui import QColor
from Qt.QtCore import QModelIndex, Qt, QSortFilterProxyModel, QAbstractListModel, QRegExp


class TagModel(QAbstractListModel):
    def __init__(self, model_data=[], parent=None):
        super(TagModel, self).__init__(parent)
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
        row = index.row()
        if value and role == Qt.UserRole:
            if isinstance(value, basestring):
                self.model_data[row].text = value
            elif isinstance(value, QColor):
                self.model_data[row].color = value
            try:
                self.dataChanged.emit(index, index)
            except:
                self.dataChanged.emit(index, index, 0)
            return True

    def remove_all(self):
        for i in xrange(self.rowCount()):
            self.removeRows(0, 1)


class TagProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(TagProxyModel, self).__init__(parent)
        self.regexp = QRegExp()
        self.regexp.setCaseSensitivity(Qt.CaseInsensitive)
        self.regexp.setPatternSyntax(QRegExp.RegExp)

    def filterAcceptsRow(self, sourceRow, sourceParent):
        """
        :type sourceRow:
        :type sourceParent:
        :rtype: bool
        """
        index = self.sourceModel().index(sourceRow, 0, sourceParent)
        item = self.sourceModel().data(index)
        if self.regexp.isEmpty():
            return True
        else:
            return self.regexp.exactMatch(item.name)

    def set_filter(self, regexp):
        """
        filter names
        Args:
            regexp:  <str>
        Returns:
        """
        regexp = ".*%s.*" % regexp if regexp else ""
        self.regexp.setPattern(regexp)
        self.invalidateFilter()
