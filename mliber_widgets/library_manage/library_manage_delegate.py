# -*- coding:utf-8 -*-
from PySide.QtWidgets import *
from PySide.QtGui import *
from PySide.QtCore import *
from mliber_libs.qt_libs.resize_pixmap_to_label import resize_pixmap_to_label


class CellLibrary(QWidget):
    def __init__(self, parent=None):
        super(CellLibrary, self).__init__(parent)
        main_layout = QVBoxLayout(self)
        self.icon_label = QLabel(self)
        self.name_label = QLabel(self)
        main_layout.addWidget(self.icon_label)
        main_layout.addWidget(self.name_label)

    def set_icon(self, icon_path):
        """
        设置显示图片
        :return:
        """
        pix_map = QPixmap(icon_path)
        scaled = resize_pixmap_to_label(pix_map, self.icon_label)
        self.icon_label.setPixmap(scaled)

    def set_name(self, name):
        """
        设置名字
        :return:
        """
        self.name_label.setText(name)


class UserManageDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(UserManageDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        editor = CellLibrary(parent)
        return editor

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        item = index.model().data(index, Qt.UserRole)
        editor.set_icon(item.icon_path)
        editor.set_name(item.name)
        editor.blockSignals(False)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    # def sizeHint(self, option, index):
    #     return QSize(160, 20)
