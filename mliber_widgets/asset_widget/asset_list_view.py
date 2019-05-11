# -*- coding:utf-8 -*-
from Qt.QtWidgets import QListView, QAbstractItemView, QApplication, QMenu, QAction, QInputDialog
from Qt.QtCore import QSize, Signal, Qt, QModelIndex
from Qt.QtGui import QCursor
from asset_model import AssetModel, AssetProxyModel
from asset_delegate import AssetDelegate
from mliber_conf import mliber_config
import mliber_global
from mliber_libs.os_libs.path import Path
import mliber_resource
from mliber_api.database_api import Database
from mliber_libs.qt_libs.image_server import ImageCacheThreadsServer

DEFAULT_ICON_SIZE = 200


class AssetListItem(object):
    def __init__(self, asset):
        """
        :param asset: <Asset>
        """
        self.asset = asset
        self.icon_path = mliber_resource.icon_path("image.png")
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


class AssetListView(QListView):
    MAX_ICON_SIZE = 256
    MIN_ICON_SIZE = 128
    double_clicked = Signal()
    add_tag_signal = Signal(basestring)
    leftPressed = Signal(QModelIndex)

    def __init__(self, parent=None):
        super(AssetListView, self).__init__(parent)
        self.image_server = None
        self.assets = []
        icon_size = QSize(DEFAULT_ICON_SIZE, DEFAULT_ICON_SIZE)
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
        # set style
        self.set_style()
        # set signals
        self.set_signals()
        # start image cache thread
        self.start_image_cache_thread()

    @property
    def db(self):
        database = mliber_global.app().value("mliber_database")
        return Database(database)

    @property
    def library(self):
        return mliber_global.library()

    @property
    def user(self):
        return mliber_global.user()

    def start_image_cache_thread(self):
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
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.leftPressed.connect(self.test)

    def test(self, index):
        item = self.item_of_index(index)
        asset = item.asset
        print asset.tags

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
        return Path(asset_path).join("thumbnail.png")

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
            if Path(icon_path).isfile():
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
        model = self.model().sourceModel()
        item = model.model_data[index.row()]
        return item

    def _add_tag_of_asset(self, asset, tag_name):
        """
        :return:
        """
        tag_ids = [tag.id for tag in asset.tags]
        db = self.db
        tag = db.find_one("Tag", [["name", "=", tag_name]])
        if not tag:
            tag = db.create("Tag", {"name": tag_name})
        tag_ids.append(tag.id)
        tags = self.db.find("Tag", [["id", "in", tag_ids]])
        db.update("Asset", asset.id, {"tags": tags})
        db.close()
        
    def _add_tag(self, tag_name):
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
            self._add_tag_of_asset(asset, tag_name)
            model.setData(index, ["tag", True], Qt.UserRole)
        self.add_tag_signal.emit(tag_name)

    def _show_add_tag_widget(self):
        """
        :return:
        """
        text, ok = QInputDialog.getText(self, "Add Tag", "Input a tag name.")
        if text and ok:
            self._add_tag(text)

    def _store_asset(self, user, asset_id):
        """
        收藏asset
        :param user: <int>
        :param asset_id: <int>
        :return:
        """
        user = self.db.find_one("User", [["id", "=", user.id]])
        assets = user.assets
        asset_ids = [asset.id for asset in assets]
        if asset_id in asset_ids:
            return
        asset_ids.append(asset_id)
        db = self.db
        assets = self.db.find("Asset", [["id", "in", asset_ids]])
        db.update("User", user.id, {"assets": assets})

    def _remove_asset_from_user(self, user, asset_id):
        """
        讲资产从我的收藏中移出
        :param user:
        :param asset_id:
        :return:
        """
        user = self.db.find_one("User", [["id", "=", user.id]])
        assets = user.assets
        asset_ids = [asset.id for asset in assets]
        if asset_id in asset_ids:
            db = self.db
            asset_ids.remove(asset_id)
            assets = db.find("Asset", [["id", "in", asset_ids]])
            db.update("User", user.id, {"assets": assets})

    def _store(self, index):
        item = self.item_of_index(index)
        user = self.user
        asset = item.asset
        if not item.stored_by_me:
            self._store_asset(user, asset.id)
            self.model().sourceModel().setData(index, ["store", True], Qt.UserRole)
        else:
            self._remove_asset_from_user(user, asset.id)
            self.model().sourceModel().setData(index, ["store", False], Qt.UserRole)

    def show_context_menu(self):
        """
        显示右键菜单
        :return:
        """
        menu = QMenu()
        user = mliber_global.user()
        if user.asset_permission:
            add_tag_action = QAction("Add Tag", self, triggered=self._show_add_tag_widget)
            menu.addAction(add_tag_action)
        menu.exec_(QCursor.pos())

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
        super(AssetListView, self).mousePressEvent(event)
        point = event.pos()
        index = self.indexAt(point)
        if index.row() < 0:
            self.clearSelection()
            return
        # if event.type() == QEvent.MouseButtonPress:
        if event.button() == Qt.LeftButton:
            self.leftPressed.emit(index)
