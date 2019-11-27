# -*- coding:utf-8 -*-
from Qt.QtCore import QModelIndex, Qt, QSortFilterProxyModel, QAbstractListModel, QRegExp, QByteArray, \
    QDataStream, QIODevice, QMimeData
from mliber_site_packages import yaml


class AssetModel(QAbstractListModel):
    def __init__(self, model_data=[], parent=None):
        super(AssetModel, self).__init__(parent)
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
        if role == Qt.ToolTipRole:
            try:
                return self._build_html_for_tooltip(item)
            except:
                pass

    def flags(self, index):
        if index.isValid():
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled

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
        if role == Qt.UserRole:
            if value:
                typ, data = value
                if data and typ == "size":
                    self.model_data[row].icon_size = data
                if typ == "tag":
                    self.model_data[row].has_tag = data
                if typ == "description":
                    self.model_data[row].description = data
                if typ == "store":
                    self.model_data[row].stored_by_me = data
                if typ == "started":
                    self.model_data[row].started = data
                try:
                    self.dataChanged.emit(index, index)
                except:
                    self.dataChanged.emit(index, index, 0)
            return True

    def remove_all(self):
        for i in xrange(self.rowCount()):
            self.removeRows(0, 1)

    @staticmethod
    def _build_html_for_tooltip(item):
        """
        创建html for tooltip
        :param item: <AssetItem>
        :return:
        """
        name = item.name
        description = item.description
        elements = item.elements
        element_types = ", ".join([element.type for element in elements])
        tags = item.tags
        tag_names = ", ".join([tag.name for tag in tags])
        path = item.path
        html = "<p><font size=4 color=#fff><b>%s</b></font></p>" \
               "<p><font size=3 color=#8a8a8a>elements:</font><font color=#fff> %s</font></p>" \
               "<p><font size=3 color=#8a8a8a>    tags:</font><font color=#fff> %s</font></p>" \
               "<p><font size=3 color=#8a8a8a>description:</font><font color=#fff> %s</font></p>" \
               "<p><font size=3 color=#8a8a8a>path:</font><font color=#fff> %s</font></p>" \
               % (name, element_types, tag_names, description, path)
        return html

    def mimeTypes(self):
        types = ['application/x-pynode-item-instance']
        return types

    def mimeData(self, indexes):
        """
        Encode serialized data from the item at the given index into a QMimeData object.
        """
        data = ''
        items = list()
        for index in indexes:
            item = self.item_from_index(index)
            items.append([item.asset.id, item.asset.name])
        try:
            data += yaml.dump_all(items)  # 如果是字符串不用cPickle
        except Exception as e:
            print "Error: %s" % str(e)
        encoded_data = QByteArray()
        stream = QDataStream(encoded_data, QIODevice.WriteOnly)
        stream << data
        mime_data = QMimeData()
        mime_data.setData('application/x-pynode-item-instance', encoded_data)
        return mime_data

    def item_from_index(self, index):
        """
        get item from index
        :param index:
        :return:
        """
        row = index.row()
        return self.model_data[row]

    def supportedDropActions(self):
        """
        :return:
        """
        return Qt.MoveAction | Qt.CopyAction


class AssetProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(AssetProxyModel, self).__init__(parent)
        self.regexp = QRegExp()
        self.setDynamicSortFilter(True)
        self.setFilterKeyColumn(0)
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.setSortCaseSensitivity(Qt.CaseInsensitive)
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
