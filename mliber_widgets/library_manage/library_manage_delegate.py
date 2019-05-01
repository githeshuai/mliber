# -*- coding:utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtGui import *
from Qt.QtCore import *
from mliber_libs.qt_libs.resize_pixmap_to_label import resize_pixmap_to_label


FONT_HEIGHT = 18


class CellLibrary(QWidget):
    def __init__(self, parent=None):
        super(CellLibrary, self).__init__(parent)
        self.setAutoFillBackground(True)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(2, 0, 2, 0)
        self.icon_label = QLabel(self)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet("background: transparent;")
        self.name_label = QLabel(self)
        self.name_label.setStyleSheet("background: transparent;")
        self.name_label.setMaximumHeight(FONT_HEIGHT)
        self.name_label.setAlignment(Qt.AlignCenter)
        # add to main layout
        main_layout.addWidget(self.icon_label)
        main_layout.addWidget(self.name_label)
        main_layout.setSpacing(0)

    def set_icon(self, icon_path):
        """
        设置显示图片
        :return:
        """
        pix_map = QPixmap(icon_path)
        scaled = resize_pixmap_to_label(pix_map, self.icon_label)
        self.icon_label.setPixmap(scaled)

    def set_icon_size(self, size):
        """
        set icon label size
        :param size:
        :return:
        """
        self.icon_label.resize(size)

    def set_name(self, name):
        """
        设置名字
        :return:
        """
        self.name_label.setText(name)

    def enterEvent(self, event):
        """
        :return:
        """
        print "enter"


class LibraryManageDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(LibraryManageDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        editor = CellLibrary(parent)
        return editor

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        item = index.model().data(index, Qt.UserRole)
        editor.set_icon_size(item.icon_size)
        editor.set_icon(item.icon_path)
        editor.set_name(item.name)
        editor.blockSignals(False)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def sizeHint(self, option, index):
        item = index.model().data(index, Qt.UserRole)
        size = QSize(item.icon_size.width(), item.icon_size.height()+FONT_HEIGHT)
        return size
