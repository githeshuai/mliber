# -*- coding:utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtGui import *
from Qt.QtCore import *
from library_manage_model import LibraryManageModel
from library_manage_delegate import LibraryManageDelegate
from mliber_conf import mliber_config
import mliber_global
from mliber_libs.os_libs.path import Path
import mliber_resource


class LibraryListView(QListView):
    DEFAULT_ICON_SIZE = 180
    MAX_ICON_SIZE = 256
    MIN_ICON_SIZE = 32

    def __init__(self, parent=None):
        super(LibraryListView, self).__init__(parent)
        icon_size = QSize(self.DEFAULT_ICON_SIZE, self.DEFAULT_ICON_SIZE)
        self.setIconSize(icon_size)
        self.setMouseTracking(True)
        self.setSpacing(4)
        self.setSelectionRectVisible(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        # show data
        self.show_data()
        # set style
        self.set_style()

    def set_style(self):
        """
        set style sheet
        :return:
        """
        self.setStyleSheet(mliber_config.LIST_VIEW_STYLE)

    @staticmethod
    def _get_model_data():
        """
        获取所有的library
        :return:
        """
        app = mliber_global.app()
        db = app.value("mliber_database")
        libraries = db.find("Library", [])
        return libraries

    def _set_model(self):
        """
        设置model
        :return:
        """
        libraries = self._get_model_data()
        model_data = list()
        for lib in libraries:
            name = lib.name
            icon_path = Path(mliber_global.public_dir()).join("library/%s.png" % name)
            if not Path(icon_path).isfile():
                icon_path = mliber_resource.icon_path("image.png")
            lib.icon_path = icon_path
            lib.icon_size = self.iconSize()
            model_data.append(lib)
        model = LibraryManageModel(model_data, self)
        self.setModel(model)

    def _set_delegate(self):
        """
        设置代理
        :return:
        """
        delegate = LibraryManageDelegate(self)
        self.setItemDelegate(delegate)
        self.show_delegate()

    def show_delegate(self):
        """
        show delegate
        :return:
        """
        for row in xrange(self.model().rowCount()):
            self.openPersistentEditor(self.model().index(row, 0))

    def show_data(self):
        """
        show data in list view
        :return:
        """
        self._set_model()
        self._set_delegate()
        self.show_delegate()

    def set_item_size(self, size):
        """
        set item size
        :param size:
        :return:
        """
        source_model = self.model()
        row_count = source_model.rowCount()
        if not row_count:
            return
        if size == self.iconSize():
            return
        self.setIconSize(size)
        for row in xrange(row_count):
            index = source_model.index(row, 0)
            source_model.setData(index, size, Qt.UserRole)

    def wheelEvent(self, event):
        zoom_amount = self.iconSize().width()
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier or modifiers == Qt.AltModifier:
            if not self.model():
                return
            row_count = self.model().rowCount()
            if not row_count:
                return
            degrees = event.delta() / 8
            step = degrees / 15
            delta = step * 8
            zoom_amount += delta
            if zoom_amount > self.MAX_ICON_SIZE:
                zoom_amount = self.MAX_ICON_SIZE
            if zoom_amount < self.MIN_ICON_SIZE:
                zoom_amount = self.MIN_ICON_SIZE
            size = QSize(zoom_amount, zoom_amount)
            self.set_item_size(size)
            # self.set_toast("Size: {0}%".format(int(zoom_amount/self.DEFAULT_ICON_SIZE*100)))
        else:
            QListView.wheelEvent(self, event)
