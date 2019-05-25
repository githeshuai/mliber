# -*- coding:utf-8 -*-
import logging
from datetime import datetime
from Qt.QtWidgets import QListView, QAbstractItemView, QApplication, QMenu, QAction, QInputDialog
from Qt.QtCore import QSize, Signal, Qt, QModelIndex
from Qt.QtGui import QCursor
from asset_model import AssetModel, AssetProxyModel
from asset_delegate import AssetDelegate
from create_tag_widget import CreateTagWidget
from mliber_conf import mliber_config
import mliber_global
import mliber_resource
import mliber_utils
from mliber_libs.dcc import Dcc
from mliber_libs.os_libs.path import Path
from mliber_api.api_utils import add_tag_of_asset
from mliber_libs.qt_libs.image_server import ImageCacheThreadsServer
from mliber_conf import templates
from mliber_parse.element_type_parser import ElementType
from mliber_parse.library_parser import Library
from mliber_qt_components.delete_widget import DeleteWidget
from mliber_qt_components.messagebox import MessageBox

DEFAULT_ICON_SIZE = 128


class AssetListItem(object):
    def __init__(self, asset):
        """
        :param asset: <Asset>
        """
        self.asset = asset
        self.icon_path = None
        self.icon_size = QSize(DEFAULT_ICON_SIZE, DEFAULT_ICON_SIZE)
        self.has_tag = True if self.asset.tags else False
        self.has_description = True if self.asset.description else False
        self.stored_by_me = self.is_stored_by_me()

    def is_stored_by_me(self):
        """
        是否被自己收藏
        :return:
        """
        masters = self.asset.master
        if masters:
            master_ids = [master.id for master in masters]
            user = mliber_global.user()
            if user.id in master_ids:
                return True
        return False

    def __getattr__(self, item):
        """
        :param item:
        :return:
        """
        if item == "path":
            library = mliber_global.library()
            root_path = library.root_path()
            return self.asset.path.format(root=root_path)
        return getattr(self.asset, item)


class AssetListView(QListView):
    MAX_ICON_SIZE = 256
    MIN_ICON_SIZE = 128
    add_tag_signal = Signal(basestring)
    left_pressed = Signal(list)
    selection_changed = Signal(int)

    def __init__(self, parent=None):
        super(AssetListView, self).__init__(parent)
        self.image_server = None
        self._engine = Dcc.engine()
        self.assets = []
        icon_size = QSize(DEFAULT_ICON_SIZE, DEFAULT_ICON_SIZE)
        self.setIconSize(icon_size)
        self.setMouseTracking(True)
        self.setSpacing(8)
        self.setSelectionRectVisible(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        # set style
        self._set_style()
        # set signals
        self._set_signals()
        # start image cache thread
        self._start_image_cache_thread()

    @property
    def library(self):
        return mliber_global.library()

    @property
    def user(self):
        return mliber_global.user()

    def _start_image_cache_thread(self):
        """
        获取刷新图片线程
        :return:
        """
        self.image_server = ImageCacheThreadsServer()
        self.image_server.cache_done_signal.connect(self._img_cached_done)

    def _img_cached_done(self, *args):
        """
        当图片缓存成功，刷新ui
        :param args:
        :return:
        """
        source_model = self.model().sourceModel()
        for row in xrange(source_model.rowCount()):
            index = source_model.index(row, 0)
            source_model.dataChanged.emit(index, index)

    def _set_style(self):
        """
        set style sheet
        :return:
        """
        self.setStyleSheet(mliber_config.LIST_VIEW_STYLE)

    def _set_signals(self):
        """
        信号链接
        :return:
        """
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
        self.doubleClicked.connect(self._on_item_double_clicked)

    def _on_item_double_clicked(self, index):
        """
        双击的时候
        :param index:
        :return:
        """
        if index.row() < 0:
            return
        source_model = self.model().sourceModel()
        source_index = self.model().mapToSource(index)
        asset = source_model.model_data[source_index.row()].asset
        element_type = Library(self.library.type).double_clicked_type()
        hook = Library(self.library.type).double_clicked_hook()
        with mliber_global.db() as db:
            self._run_hook(db, asset, element_type, hook)

    def _on_selection_changed(self):
        """
        :return:
        """
        num = len(self._selected_rows())
        self.selection_changed.emit(num)

    def _get_asset_path(self, asset):
        """
        获取asset的绝对路径
        :param asset:
        :return:
        """
        relative_path = asset.path
        abs_path = relative_path.format(root=self.library.root_path())
        return abs_path

    def _get_asset_icon_path(self, asset):
        """
        获取asset的图标位置
        :param asset:
        :return:
        """
        asset_path = self._get_asset_path(asset)
        thumbnail_pattern = templates.THUMBNAIL_PATH.format(asset_dir=asset_path, asset_name=asset.name)
        return Path(thumbnail_pattern).parent()

    def set_assets(self, assets):
        """
        外部接口
        :param assets:
        :return:
        """
        self.assets = assets
        self._set_model(self.assets)
        self._set_delegate()

    def _get_model_data(self, assets):
        """
        获取所有的library
        :return:
        """
        model_data = list()
        for asset in assets:
            item = AssetListItem(asset)
            icon_path = self._get_asset_icon_path(asset)
            item.icon_path = icon_path
            item.icon_size = self.iconSize()
            model_data.append(item)
        return model_data

    def _set_model(self, assets):
        """
        设置model
        :return:
        """
        model_data = self._get_model_data(assets)
        model = AssetModel(model_data, self)
        proxy_model = AssetProxyModel(self)
        proxy_model.setSourceModel(model)
        self.setModel(proxy_model)
        # selection changed
        selection_model = self.selectionModel()
        selection_model.selectionChanged.connect(self._on_selection_changed)

    def _set_delegate(self):
        """
        设置代理
        :return:
        """
        delegate = AssetDelegate(self)
        delegate.store_clicked.connect(self._store)
        self.setItemDelegate(delegate)
        self.show_delegate()

    def show_delegate(self):
        """
        show delegate
        :return:
        """
        for row in xrange(self.model().rowCount()):
            self.openPersistentEditor(self.model().index(row, 0))

    def add_asset(self, asset):
        """
        :param asset: Asset instance
        :return:
        """
        if asset.id in [a.id for a in self.assets]:
            return
        item = AssetListItem(asset)
        icon_path = self._get_asset_icon_path(asset)
        item.icon_path = icon_path
        item.icon_size = self.iconSize()
        source_model = self.model().sourceModel()
        source_model.insertRows(source_model.rowCount(), 1, [item])
        self.show_delegate()

    def _set_item_size(self, size):
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
            source_model.setData(index, ["size", size], Qt.UserRole)

    def _selected_indexes(self):
        """
        获取选择的index
        :return:
        """
        selected_indexes = self.selectedIndexes()
        return selected_indexes

    def _selected_rows(self):
        """
        获取选择的行
        :return:
        """
        selected_indexes = self._selected_indexes()
        src_indexes = [self.model().mapToSource(index) for index in selected_indexes]
        rows = list(set([index.row() for index in src_indexes]))
        return rows

    def selected_items(self):
        """
        获取选择的library
        :return:
        """
        selected_items = list()
        selected_rows = self._selected_rows()
        if selected_rows:
            selected_items = [self.model().sourceModel().model_data[row] for row in selected_rows]
        return selected_items

    def selected_assets(self):
        """
        获取selected library
        :return:
        """
        selected_items = self.selected_items()
        selected_assets = [selected_item.asset for selected_item in selected_items]
        return selected_assets
    
    @property
    def asset_names(self):
        """
        获取所有的asset name
        :return:
        """
        asset_names = [asset.name for asset in self.assets]
        return asset_names
    
    def item_of_index(self, index):
        """
        根据index 获取item
        :param index: <QModelIndex>
        :return:
        """
        src_index = self.model().mapToSource(index)
        source_model = self.model().sourceModel()
        item = source_model.model_data[src_index.row()]
        return item
        
    def _add_tag(self, tag_names):
        """
        给选中的资产添加tag
        :return:
        """
        selected_indexes = self._selected_indexes()
        if not selected_indexes:
            return
        for index in selected_indexes:
            model = self.model().sourceModel()
            item = model.model_data[index.row()]
            asset = item.asset
            with mliber_global.db() as db:
                add_tag_of_asset(db, asset, tag_names)
            model.setData(index, ["tag", True], Qt.UserRole)
        self.add_tag_signal.emit(tag_names)

    def _show_add_tag_widget(self):
        """
        :return:
        """
        selected_assets = self.selected_assets()
        if not selected_assets:
            return
        asset_ids = [asset.id for asset in selected_assets]
        with mliber_global.db() as db:
            assets = db.find("Asset", [["id", "in", asset_ids]])
        tags = []
        for asset in assets:
            tags.extend(asset.tags)
        create_tag_dialog = CreateTagWidget(self)
        for tag in tags:
            create_tag_dialog.add_tag(tag.name, tag.color())
        create_tag_dialog.ok_clicked.connect(self._add_tag)
        create_tag_dialog.exec_()

    @staticmethod
    def _store_asset(user, asset_id):
        """
        收藏asset
        :param user: <int>
        :param asset_id: <int>
        :return:
        """
        with mliber_global.db() as db:
            user = db.find_one("User", [["id", "=", user.id]])
            assets = user.assets
            asset_ids = [asset.id for asset in assets]
            if asset_id in asset_ids:
                return
            asset_ids.append(asset_id)
            db = db
            assets = db.find("Asset", [["id", "in", asset_ids]])
            db.update("User", user.id, {"assets": assets})

    @staticmethod
    def _remove_asset_from_user(user, asset_id):
        """
        讲资产从我的收藏中移出
        :param user:
        :param asset_id:
        :return:
        """
        with mliber_global.db() as db:
            user = db.find_one("User", [["id", "=", user.id]])
            assets = user.assets
            asset_ids = [asset.id for asset in assets]
            if asset_id in asset_ids:
                asset_ids.remove(asset_id)
                assets = db.find("Asset", [["id", "in", asset_ids]])
                db.update("User", user.id, {"assets": assets})

    def _store(self, index):
        """
        收藏
        :param index: QModelIndex
        :return:
        """
        item = self.item_of_index(index)
        user = self.user
        asset = item.asset
        if not item.stored_by_me:
            self._store_asset(user, asset.id)
            self.model().sourceModel().setData(index, ["store", True], Qt.UserRole)
        else:
            self._remove_asset_from_user(user, asset.id)
            self.model().sourceModel().setData(index, ["store", False], Qt.UserRole)

    def _single_selection_actions(self, asset):
        """
        选择一个资产的时候，右键菜单的action
        :return:
        """
        q_actions = list()
        elements = asset.elements
        for element in elements:
            actions = ElementType(element.type).import_actions_of_engine(self._engine)
            for action in actions:
                q_action = QAction(action.name, self, triggered=self._on_action_triggered)
                q_action.type = element.type
                q_action.hook = action.hook
                q_actions.append(q_action)
        return q_actions

    def _multi_selection_actions(self):
        """
        :return:
        """
        q_actions = list()
        support_types = Library(self.library.type).types()
        for typ in support_types:
            actions = ElementType(typ).import_actions_of_engine(self._engine)
            for action in actions:
                q_action = QAction(action.name, self, triggered=self._on_action_triggered)
                q_actions.append(q_action)
                q_action.type = typ
                q_action.hook = action.hook
        return q_actions

    def _show_context_menu(self):
        """
        显示右键菜单
        :return:
        """
        selected_assets = self.selected_assets()
        if not selected_assets:
            return
        menu = QMenu(self)
        user = mliber_global.user()
        if user.asset_permission:
            add_tag_action = QAction("Add Tag", self, triggered=self._show_add_tag_widget)
            menu.addAction(add_tag_action)
        open_action = QAction("Open in Explorer", self, triggered=self._open_in_explorer)
        menu.addAction(open_action)
        if user.asset_permission:
            delete_action = QAction(mliber_resource.icon("delete.png"), "Send to Trash", self,
                                    triggered=self._show_delete_widget)
            menu.addAction(delete_action)
        menu.addSeparator()
        # add custom action
        asset_ids = [asset.id for asset in selected_assets]
        with mliber_global.db() as db:
            assets = db.find("Asset", [["id", "in", asset_ids]])
            if len(assets) == 1:
                q_actions = self._single_selection_actions(assets[0])
            else:
                q_actions = self._multi_selection_actions()
        for q_action in q_actions:
            menu.addAction(q_action)
        menu.exec_(QCursor.pos())

    def _on_action_triggered(self):
        """
        :return:
        """
        element_type = self.sender().type
        hook = self.sender().hook
        assets = self.selected_assets()
        with mliber_global.db() as db:
            for asset in assets:
                self._run_hook(db, asset, element_type, hook)

    def _run_hook(self, db, asset, element_type, hook):
        """
        :param db:
        :param asset: <Asset>
        :param element_type: <str>
        :param hook: <str> hook name
        :return:
        """
        element = db.find_one("Element", [["type", "=", element_type], ["asset_id", "=", asset.id]])
        if not element:
            logging.warning("Element type: %s not found." % element_type)
            return
        path = element.path
        if path:
            path = path.format(root=self.library.root_path())
        start = element.start
        end = element.end
        asset_name = asset.name
        try:
            hook_module = mliber_utils.load_hook(hook)
            if not hook_module:
                logging.error("Hook: %s not found." % hook)
                return
            reload(hook_module)
            hook_instance = hook_module.Hook(path, "", start, end, asset_name)
            hook_instance.main()
        except Exception as e:
            logging.error(str(e))

    def _show_delete_widget(self):
        """
        显示delete widget
        """
        delete_widget = DeleteWidget(self)
        delete_widget.accept_signal.connect(self._delete_asset)
        delete_widget.exec_()
        
    def _delete_asset(self, delete_source):
        """
        删除资产
        :param delete_source: 是否删除源文件
        :return: 
        """
        source_model = self.model().sourceModel()
        deleted = True
        for index, row in enumerate(self._selected_rows()):
            asset = source_model.model_data[row]
            with mliber_global.db() as db:
                db.update("Asset", asset.id, {"status": "Disable",
                                              "updated_by": self.user.id,
                                              "updated_at": datetime.now()})
                source_model.removeRows(row - index, 1)
                elements = db.find("Element", [["asset_id", "=", asset.id], ["status", "=", "Active"]])
                for element in elements:
                    db.update("Element", element.id, {"status": "Disable", "updated_by": self.user.id,
                                                      "updated_at": datetime.now()})
            if delete_source:
                asset_path = asset.path.format(root=self.library.root_path())
                try:
                    Path(asset_path).remove()
                except WindowsError as e:
                    print str(e)
                    deleted = False
        if not deleted:
            MessageBox.warning(self, "Warning", "Storage files delete Failed，Please delete it manual.")

    def _open_in_explorer(self):
        """
        在文件系统中打开
        :return:
        """
        selected_items = self.selected_items()
        if not selected_items:
            return
        item = selected_items[0]
        path = item.path
        Path(path).open()

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
            self._set_item_size(size)
        else:
            QListView.wheelEvent(self, event)

    def mousePressEvent(self, event):
        """
        当鼠标左键点击到空白处，取消选择
        :param event:
        :return:
        """
        super(AssetListView, self).mousePressEvent(event)
        point = event.pos()
        index = self.indexAt(point)
        if index.row() < 0:
            self.clearSelection()
            return
        # if event.type() == QEvent.MouseButtonPress:
        if event.button() == Qt.LeftButton:
            item = self.item_of_index(index)
            asset = item.asset
            self.left_pressed.emit([asset])
