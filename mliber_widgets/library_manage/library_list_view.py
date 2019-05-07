# -*- coding:utf-8 -*-
from datetime import datetime
from Qt.QtWidgets import QListView, QAbstractItemView, QApplication
from Qt.QtCore import QSize, Signal, Qt
from library_manage_model import LibraryManageModel, LibraryManageProxyModel
from library_manage_delegate import LibraryManageDelegate
from mliber_conf import mliber_config
import mliber_global
import mliber_utils
from mliber_libs.os_libs.path import Path
import mliber_resource
from mliber_libs.os_libs import system
from mliber_qt_components.messagebox import MessageBox
from mliber_api.database_api import Database

DEFAULT_ICON_SIZE = 200


class LibraryListItem(object):
    def __init__(self, library):
        """
        :param library: <Library>
        """
        self.library = library
        self.icon_path = mliber_resource.icon_path("image.png")
        self.icon_size = QSize(DEFAULT_ICON_SIZE, DEFAULT_ICON_SIZE)


class LibraryListView(QListView):

    MAX_ICON_SIZE = 256
    MIN_ICON_SIZE = 128
    double_clicked = Signal()

    def __init__(self, parent=None):
        super(LibraryListView, self).__init__(parent)
        icon_size = QSize(DEFAULT_ICON_SIZE, DEFAULT_ICON_SIZE)
        self.setIconSize(icon_size)
        self.setMouseTracking(True)
        self.setSpacing(4)
        self.setSelectionRectVisible(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        # show data
        self.show_data()
        # set style
        self.set_style()
        # set signals
        self.set_signals()
    
    @property
    def db(self):
        database = mliber_global.app().value("mliber_database")
        return Database(database)
    
    def set_style(self):
        """
        set style sheet
        :return:
        """
        self.setStyleSheet(mliber_config.LIST_VIEW_STYLE)

    def set_signals(self):
        """
        信号链接
        :return:
        """
        self.doubleClicked.connect(self.set_global_library)

    def set_global_library(self):
        """
        set global library
        :return:
        """
        selected_library = self.selected_library()
        if not selected_library:
            return
        # set global
        app = mliber_global.app()
        app.set_value(mliber_library=selected_library)
        # write history
        mliber_utils.write_history(library_id=selected_library.id)
        self.double_clicked.emit()

    @staticmethod
    def _get_library_icon_path(library_name):
        """
        获取library 图标路径
        :return:
        """
        icon_path = Path(mliber_global.public_dir()).join("library/%s.png" % library_name)
        return icon_path

    def _get_model_data(self):
        """
        获取所有的library
        :return:
        """
        model_data = list()
        libraries = self.db.find("Library", [["status", "=", "Active"]])
        for library in libraries:
            item = LibraryListItem(library)
            icon_path = self._get_library_icon_path(library.name)
            if Path(icon_path).isfile():
                item.icon_path = icon_path
            item.icon_size = self.iconSize()
            model_data.append(item)
        return model_data

    def _set_model(self):
        """
        设置model
        :return:
        """
        model_data = self._get_model_data()
        model = LibraryManageModel(model_data, self)
        proxy_model = LibraryManageProxyModel(self)
        proxy_model.setSourceModel(model)
        self.setModel(proxy_model)

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

    def _selected_rows(self):
        """
        获取选择的行
        :return:
        """
        selected_indexes = self.selectedIndexes()
        src_indexes = [self.model().mapToSource(index) for index in selected_indexes]
        rows = list(set([index.row() for index in src_indexes]))
        return rows

    def selected_item(self):
        """
        获取选择的library
        :return:
        """
        selected_rows = self._selected_rows()
        if not selected_rows:
            return
        row = selected_rows[0]
        return self.model().sourceModel().model_data[row]

    def selected_library(self):
        """
        获取selected library
        :return:
        """
        selected_item = self.selected_item()
        if selected_item:
            return selected_item.library

    def libraries(self):
        """
        获取所有的library
        :return:
        """
        items = self.model().sourceModel().model_data
        return [item.library for item in items]

    def library_names(self):
        """
        获取所有的library name
        :return: <list>
        """
        libraries = self.libraries()
        return [library.name for library in libraries]

    @staticmethod
    def _get_library_paths(libraries, attr):
        """
        :return:
        """
        paths = list()
        for library in libraries:
            path = getattr(library, attr)
            if path:
                paths.append(path.replace("\\", "/"))
        return paths

    def library_paths(self):
        """
        获取已经存在的library的paths
        :return: <dict>
        """
        paths = dict()
        libraries = self.libraries()
        windows_paths = self._get_library_paths(libraries, "windows_path")
        linux_paths = self._get_library_paths(libraries, "linux_path")
        mac_paths = self._get_library_paths(libraries, "mac_path")
        paths["windows"] = windows_paths
        paths["linux"] = linux_paths
        paths["mac"] = mac_paths
        return paths

    def validate_path_unique(self, windows_path, linux_path, mac_path):
        """
        检查是否已经有重复的路径，并且检查该路径是否已经存在
        :param windows_path:
        :param linux_path:
        :param mac_path:
        :return:
        """
        exist_paths = self.library_paths()
        if windows_path in exist_paths.get("windows") or \
                linux_path in exist_paths.get("linux") or \
                mac_path in exist_paths.get("mac"):
            MessageBox.warning(self, "warning", u"path exist !")
            return False
        return True

    def validate_path_can_be_created(self, windows_path, linux_path, mac_path):
        """
        检查该路径是否可正常创建
        :param windows_path:
        :param linux_path:
        :param mac_path:
        :return:
        """
        operation_system = system.operation_system()
        try:
            if operation_system == "windows":
                Path(windows_path).makedirs()
            elif operation_system == "linux":
                Path(linux_path).makedirs()
            elif operation_system == "mac":
                Path(mac_path).makedirs()
            return True
        except WindowsError as e:
            MessageBox.critical(self, "Error", str(e))
            return False

    def update_library(self, name, typ, windows_path, linux_path, mac_path, icon_path, description=""):
        """
        刷新library data
        :param name: <str>
        :param typ: <str>
        :param windows_path: <str>
        :param linux_path: <str>
        :param mac_path: <str>
        :param icon_path: <str>
        :param description: <str>
        :return:
        """
        if not self.validate_path_can_be_created(windows_path, linux_path, mac_path):
            return
        selected_item = self.selected_item()
        user = mliber_global.app().value("mliber_user")
        now = datetime.now()
        data = {"name": name, "type": typ, "windows_path": windows_path, "linux_path": linux_path,
                "mac_path": mac_path, "description": description, "updated_by": user.id, "updated_at": now}
        try:
            self.db.update("Library", selected_item.library.id, data)
            library_icon_path = self._get_library_icon_path(name)
            if icon_path != library_icon_path:
                if Path(icon_path).isfile():
                    Path(icon_path).copy_to(library_icon_path)
            return True
        except RuntimeError as e:
            MessageBox.critical(self, "Error", str(e))
            return False

    def append_library(self, name, typ, windows_path, linux_path, mac_path, icon_path, description="", status="Active"):
        """
        添加一个library
        :param name: <str>
        :param typ: <str>
        :param windows_path: <str>
        :param linux_path: <str>
        :param mac_path: <str>
        :param icon_path: <str>
        :param status: <str> Active or disable
        :param description: <str>
        :return:
        """
        # 现在数据库里添加
        if name in self.library_names():
            MessageBox.warning(self, "warning", u"%s exist !" % name)
            return False
        # 因为library的name /windows path/linux path/mac path都是唯一性，所以添加之前先检查是否是唯一的
        if not self.validate_path_unique(windows_path, linux_path, mac_path):
            return
        if not self.validate_path_can_be_created(windows_path, linux_path, mac_path):
            return
        app = mliber_global.app()
        user = app.value("mliber_user")
        library = self.db.create("Library", {"name": name, "type": typ, "windows_path": windows_path,
                                             "linux_path": linux_path, "mac_path": mac_path, "status": status,
                                             "description": description, "created_by": user.id})
        # 将icon 拷贝到 public dir
        if icon_path and Path(icon_path).isfile():
            library_icon_path = self._get_library_icon_path(name)
            Path(icon_path).copy_to(library_icon_path)
        else:
            library_icon_path = mliber_resource.icon_path("image.png")
        item = LibraryListItem(library)
        item.icon_path = library_icon_path
        item.icon_size = self.iconSize()
        # 在model里添加
        source_model = self.model().sourceModel()
        source_model.insertRows(source_model.rowCount(), 1, [item])
        self.show_delegate()
        return True

    def refresh_ui(self):
        """
        刷新list view
        :return:
        """
        self.show_data()

    def wheelEvent(self, event):
        """
        鼠标滚轮事件
        :param event:
        :return:
        """
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
            delta = step * 16
            zoom_amount += delta
            if zoom_amount > self.MAX_ICON_SIZE:
                zoom_amount = self.MAX_ICON_SIZE
            if zoom_amount < self.MIN_ICON_SIZE:
                zoom_amount = self.MIN_ICON_SIZE
            size = QSize(zoom_amount, zoom_amount)
            self.set_item_size(size)
        else:
            QListView.wheelEvent(self, event)

    def mousePressEvent(self, event):
        """
        当鼠标左键点击到空白处，取消选择
        :param event:
        :return:
        """
        super(LibraryListView, self).mousePressEvent(event)
        point = event.pos()
        index = self.indexAt(point)
        if index.row() < 0:
            self.clearSelection()

