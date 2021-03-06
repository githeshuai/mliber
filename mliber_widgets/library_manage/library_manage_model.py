# -*- coding:utf-8 -*-
from functools import partial
from Qt.QtCore import QModelIndex, Qt, QSortFilterProxyModel, QAbstractListModel, QRegExp


class LibraryManageModel(QAbstractListModel):
    def __init__(self, model_data=[], parent=None):
        super(LibraryManageModel, self).__init__(parent)
        self.model_data = model_data
        self.__parent = parent

    def rowCount(self, parent=QModelIndex()):
        return len(self.model_data)

    def data(self, index, role=Qt.UserRole):
        if not index.isValid():
            return
        row = index.row()
        item = self.model_data[row]
        library = item.library
        if role == Qt.UserRole:
            return item
        if role == Qt.ToolTipRole:
            html = "<p><font size=3 color=#8a8a8a>id:</font><font color=#fff> %s</font></p>" \
                   "<p><font size=3 color=#8a8a8a>windows:</font><font color=#fff> %s</font></p>" \
                   "<p><font size=3 color=#8a8a8a>linux:</font><font color=#fff> %s</font></p>" \
                   "<p><font size=3 color=#8a8a8a>mac:</font><font color=#fff> %s</font></p>" \
                    % (library.id, library.windows_path, library.linux_path, library.mac_path)
            return html

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

    def setData(self, index, value, role):
        row = index.row()
        if value:
            if role == Qt.UserRole:
                self.model_data[row].icon_size = value
                try:
                    self.dataChanged.emit(index, index)
                except:
                    self.dataChanged.emit(index, index, 0)
            return True

    def remove_all(self):
        for i in xrange(self.rowCount()):
            self.removeRows(0, 1)


class LibraryManageProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(LibraryManageProxyModel, self).__init__(parent)
        self.regexp = QRegExp()
        self.regexp.setCaseSensitivity(Qt.CaseInsensitive)
        self.regexp.setPatternSyntax(QRegExp.RegExp)
        self.filter_type = None

    def set_filter_type(self, filter_type):
        """
        :param filter_type: <str> name or type
        :return:
        """
        self.filter_type = filter_type

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
            if self.filter_type == "type":
                return self.regexp.exactMatch(item.type)
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
