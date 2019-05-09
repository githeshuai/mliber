# -*- coding:utf-8 -*-
from datetime import datetime
from Qt.QtWidgets import QListView, QAbstractItemView, QApplication
from Qt.QtCore import QSize, Signal, Qt
from asset_model import AssetModel, AssetProxyModel
from asset_delegate import AssetDelegate
from mliber_conf import mliber_config
import mliber_global
import mliber_utils
from mliber_libs.os_libs.path import Path
import mliber_resource
from mliber_libs.os_libs import system
from mliber_qt_components.messagebox import MessageBox
from mliber_api.database_api import Database

DEFAULT_ICON_SIZE = 200


class AssetListItem(object):
    def __init__(self, asset):
        """
        :param asset: <Asset>
        """
        self.asset = asset
        self.icon_path = mliber_resource.icon_path("image.png")
        self.icon_size = QSize(DEFAULT_ICON_SIZE, DEFAULT_ICON_SIZE)

    @property
    def user(self):
        return mliber_global.app().value("mliber_user")

    def has_tag(self):
        """
        判断是否加了标签
        :return:
        """
        value = True if self.asset.tags else False
        return value

    def has_description(self):
        """
        判断是否有评论
        :return:
        """
        value = True if self.asset.description else False
        return value

    def stored_by_me(self):
        """
        是否被自己收藏
        :return:
        """
        masters = self.asset.master
        if masters:
            master_ids = [master.id for master in masters]
            if self.user.id in master_ids:
                return True
        return False


class AssetListView(QListView):
    MAX_ICON_SIZE = 256
    MIN_ICON_SIZE = 128
    double_clicked = Signal()

    def __init__(self, parent=None):
        super(AssetListView, self).__init__(parent)
        self.assets = None
        icon_size = QSize(DEFAULT_ICON_SIZE, DEFAULT_ICON_SIZE)
        self.setIconSize(icon_size)
        self.setMouseTracking(True)
        self.setSpacing(4)
        self.setSelectionRectVisible(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setSelectionMode(QAbstractItemView.MultiSelection)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        # set style
        self.set_style()
        # set signals
        self.set_signals()

    @property
    def db(self):
        database = mliber_global.app().value("mliber_database")
        return Database(database)

    @property
    def library(self):
        return mliber_global.app().value("mliber_library")

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
        return

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
