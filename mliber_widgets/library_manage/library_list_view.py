# -*- coding:utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtGui import *
from Qt.QtCore import *
import mliber_global
from mliber_libs.os_libs.system import operation_system
from mliber_custom.public_path import PUBLIC_PATH


class LibraryListView(QListView):
    DEFAULT_ICON_SIZE = 90
    MAX_ICON_SIZE = 256
    MIN_ICON_SIZE = 32

    def __init__(self, parent=None):
        super(LibraryListView, self).__init__(parent)
        self.icon_size = QSize(self.DEFAULT_ICON_SIZE, self.DEFAULT_ICON_SIZE)
        self.setIconSize(self.icon_size)
        self.setSpacing(0)
        self.setMouseTracking(True)
        self.setSpacing(2)
        self.setSelectionRectVisible(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    @staticmethod
    def get_model_data():
        """
        获取所有的library
        :return:
        """
        app = mliber_global.app()
        db = app.get("mliber_database")
        libraries = db.find("Library", [])
        return libraries

    def set_model(self):
        """
        设置model
        :return:
        """
        pass