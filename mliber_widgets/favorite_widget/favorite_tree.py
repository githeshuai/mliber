#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date      : 2019-11-26 12:43
# Author    : Mr. He
# Version   :
# Usage     : 
# Notes     :

# Import built-in modules
from datetime import datetime
from itertools import tee
# Import third-party modules
from Qt.QtWidgets import QTreeWidget, QTreeWidgetItem, QFrame, QAbstractItemView, QInputDialog, QDialog, \
    QFormLayout, QLineEdit, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QMenu, QAction
from Qt.QtGui import QCursor
from Qt.QtCore import Signal, Qt, QDataStream, QIODevice
# Import local modules
import mliber_global
import mliber_resource
from mliber_site_packages import yaml
from mliber_qt_components.messagebox import MessageBox


class CreateFavoriteWidget(QDialog):
    def __init__(self, parent=None):
        super(CreateFavoriteWidget, self).__init__(parent)
        self._setup_ui()
        self._build_connections()
        self.name = None
        self.description = ""

    def _setup_ui(self):
        """
        setup ui
        :return:
        """
        self.setWindowTitle("Create My Favorite")
        self.resize(400, 200)
        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        self.name_le = QLineEdit(self)
        self.description_te = QTextEdit(self)
        form_layout.addRow("name", self.name_le)
        form_layout.addRow("description", self.description_te)
        # button layout
        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add", self)
        self.cancel_btn = QPushButton("Cancel", self)
        button_layout.addStretch()
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.cancel_btn)
        # add to main
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

    def _build_connections(self):
        """
        build connections
        :return:
        """
        self.add_btn.clicked.connect(self._on_add_clicked)
        self.cancel_btn.clicked.connect(self.close)

    def _on_add_clicked(self):
        """
        :return:
        """
        self.name = self.name_le.text()
        self.description = self.description_te.toPlainText()
        self.accept()


class FavoriteTreeItem(QTreeWidgetItem):
    def __init__(self, item_type="favorite", parent=None):
        super(FavoriteTreeItem, self).__init__(parent)
        self.favorite = None
        self.asset = None
        self.father = parent
        self.item_type = item_type
        self.setIcon(0, mliber_resource.icon("%s.png" % self.item_type))

    def set_favorite(self, favorite):
        """
        :param favorite: <Favorite> 表对象
        :return:
        """
        self.favorite = favorite
        self.setText(0, favorite.name)
        # html = "<p><font size=3 color=#8a8a8a>id:</font><font color=#fff> %s</font></p>" \
        #        "<p><font size=3 color=#8a8a8a>path:</font><font color=#fff> %s</font></p>" % (self.favorite.id, path)
        # self.setToolTip(0, html)

    def set_asset(self, asset):
        """
        :param asset: <Asset>
        :return:
        """
        self.asset = asset
        self.setText(0, asset.name)


class FavoriteTree(QTreeWidget):
    selection_changed = Signal(list)
    deleted_signal = Signal()
    store_signal = Signal()
    remove_from_favorite_signal = Signal()

    def __init__(self, parent=None):
        super(FavoriteTree, self).__init__(parent)
        self.setSelectionMode(self.ExtendedSelection)
        self.setFocusPolicy(Qt.NoFocus)
        self.setHeaderHidden(True)
        self.setDropIndicatorShown(True)
        self.setAcceptDrops(True)
        self.setFrameShape(QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.items_mapping = {}
        self._set_signals()

    def _set_signals(self):
        """
        set signals
        :return:
        """
        self.itemPressed.connect(self._on_item_selection_changed)

    @property
    def user(self):
        return mliber_global.user()

    def selected_items(self):
        """
        获取选中的item
        :return:
        """
        selected_items = self.selectedItems()
        return selected_items

    def selected_favorites(self):
        """
        获取选中的favorite
        :return:
        """
        selected_items = self.selected_items()
        favorites = [item.favorite for item in selected_items if item.favorite]
        return favorites

    def selected_assets(self):
        """
        get selected assets
        :return:
        """
        selected_items = self.selected_items()
        assets = [item.asset for item in selected_items if item.asset]
        return assets

    def add_favorite(self):
        """
        add favorite
        :return:
        """
        selected_item = None
        selected_items = self.selected_items()
        if selected_items:
            selected_item = selected_items[0]
        create_favorite_dialog = CreateFavoriteWidget(self)
        create_favorite_dialog.exec_()
        name = create_favorite_dialog.name
        description = create_favorite_dialog.description
        if name:
            self._add_favorite(name, description, selected_item)

    def _add_favorite(self, name, description, parent_item):
        """
        :param name:
        :param parent_item:
        :return:
        """
        parent_id = None
        if isinstance(parent_item, QTreeWidgetItem):
            parent_id = parent_item.favorite.id
        with mliber_global.db() as db:
            favorite = db.create("Favorite", {"name": name, "parent_id": parent_id,
                                              "user_id": self.user.id, "description": description})
            # 在ui上显示
            tree_widget_item = FavoriteTreeItem(parent=parent_item or self)
            tree_widget_item.set_favorite(favorite)
            self.items_mapping[name] = tree_widget_item
            if parent_item:
                parent_item.setExpanded(True)

    def search_item(self, item_text):
        """
        通过text找到item
        :param item_text:
        :return:
        """
        item = self.items_mapping.get(item_text)
        if item:
            index = self.indexFromItem(item)
            self.scrollTo(index)
            
    def refresh_data(self):
        """
        刷新数据
        :return: 
        """
        self.clear()
        if not self.user:
            return

        id_item_mapping = dict()
        items = list()
        with mliber_global.db() as db:
            favorites = db.find("Favorite", [["user_id", "=", self.user.id],
                                             ["status", "=", "Active"]])
            # 将所有的favorite添加到top level
            for favorite in favorites:
                favorite_item = FavoriteTreeItem(parent=self)
                favorite_item.set_favorite(favorite)
                self.items_mapping[favorite.name] = favorite_item
                items.append(favorite_item)
                id_item_mapping[favorite.id] = favorite_item
                # 将asset放在各自的favorite里
                assets = favorite.assets
                for asset in assets:
                    asset_item = FavoriteTreeItem("asset", parent=favorite_item)
                    asset_item.set_asset(asset)
            # 将favorite放在各自的父层级下
            for item in items:
                parent_id = item.favorite.parent_id
                if parent_id:
                    index = self.indexOfTopLevelItem(item)
                    self.takeTopLevelItem(index)
                    id_item_mapping.get(parent_id).addChild(item)

    def contextMenuEvent(self, event):
        """
        显示右键菜单
        :return:
        """
        item = self.itemAt(event.pos())

        menu = QMenu(self)
        if item.item_type == "favorite":
            add_favorite_action = QAction("Add Favorite", self, triggered=self.add_favorite)
            rename_favorite_action = QAction("Rename", self, triggered=self._rename_favorite)
            delete_action = QAction(mliber_resource.icon("delete.png"), u"Send to Trash", self,
                                    triggered=self.delete_favorite)
            menu.addAction(add_favorite_action)
            menu.addAction(rename_favorite_action)
            menu.addSeparator()
            menu.addAction(delete_action)
        else:
            remove_from_favorite_action = QAction("Remove From Favorite", self, triggered=self._remove_from_favorite)
            menu.addAction(remove_from_favorite_action)
        menu.exec_(QCursor.pos())

    def _remove_from_favorite(self):
        """
        remove form my favorite
        :return:
        """
        favorite_asset_mapping = dict()
        selected_items = self.selected_items()
        for item in selected_items:
            if item.item_type == "asset":
                asset_id = item.asset.id
                parent_item = item.father
                # remove in ui
                parent_item.removeChild(item)
                favorite = parent_item.favorite
                favorite_id = favorite.id
                if favorite_id not in favorite_asset_mapping.keys():
                    favorite_asset_mapping[favorite_id] = [asset_id]
                else:
                    favorite_asset_mapping[favorite_id].append(asset_id)

        with mliber_global.db() as db:
            for favorite_id, asset_ids in favorite_asset_mapping.iteritems():
                favorite = db.find_one("Favorite", [["id", "=", favorite_id]])
                exist_assets = favorite.assets
                exist_asset_ids = [asset.id for asset in exist_assets]
                now_asset_ids = list(set(exist_asset_ids)-set(asset_ids))
                assets = db.find("Asset", [["id", "in", now_asset_ids]])
                db.update("Favorite", favorite.id, {"assets": assets})

    def _rename_favorite(self):
        """
        修改favorite的名字
        :return:
        """
        selected_items = self.selected_items()
        if not len(selected_items) == 1:
            MessageBox.warning(self, "Warning", "Only support rename one favorite once a time.")
            return
        item = selected_items[0]
        favorite = item.favorite
        name, ok = QInputDialog.getText(self, "New favorite name", "Input a new favorite name")
        if name and ok:
            with mliber_global.db() as db:
                favorite = db.update("Favorite", favorite.id, {"name": name})
                item.set_favorite(favorite)

    def delete_favorite(self):
        """
        delete favorite
        :return:
        """
        selected_items = self.selected_items()
        if len(selected_items) != 1:
            MessageBox.warning(self, "Warning", "Only support delete one favorite once a time")
            return
        selected_item = selected_items[0]
        self.recursion_delete_favorite(selected_item.favorite)
        # 从tree widget中移除
        parent = selected_item.father
        if parent is self:
            index = self.indexOfTopLevelItem(selected_item)
            self.takeTopLevelItem(index)
        else:
            parent.removeChild(selected_item)

    def recursion_delete_favorite(self, favorite):
        """
        递归删除子类型
        :param favorite: Favorite instance
        :return:
        """
        favorites = self._get_children_favorites([favorite])
        with mliber_global.db() as db:
            for favorite in favorites:
                db.update("Favorite", favorite.id, {"status": "Disable", "updated_at": datetime.now()})

    @staticmethod
    def _get_children_favorites(favorites):
        """
        获取子类型，需要递归
        :param favorites: <list> list of Favorite
        :return:
        """
        all_favorites = list()

        def get(favorite_list):
            favorite_id_list = [favorite.id for favorite in favorite_list]
            with mliber_global.db() as db:
                children_categories = db.find("Favorite",
                                              [["parent_id", "in", favorite_id_list],
                                               ["status", "=", "Active"]])
                if children_categories:
                    all_favorites.extend(children_categories)
                    get(children_categories)

        get(favorites)
        all_favorites.extend(favorites)
        return all_favorites
    
    def _on_item_selection_changed(self):
        """
        :return: 
        """
        assets = self.selected_assets()
        selected_favorites = self.selected_favorites()
        favorites = self._get_children_favorites(selected_favorites)
        self.selection_changed.emit([favorites, assets])

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/x-pynode-item-instance'):
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('application/x-pynode-item-instance'):
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        current_item = self.itemAt(event.pos())
        if not current_item:
            return
        if current_item.item_type == "favorite":
            parent_item = current_item
        else:
            parent_item = current_item.parent()
        if event.mimeData().hasFormat('application/x-pynode-item-instance'):
            event.setDropAction(Qt.MoveAction)
            data = event.mimeData().data('application/x-pynode-item-instance')
            stream = QDataStream(data, QIODevice.ReadOnly)
            text = stream.readQString()
            asset_ids = yaml.load_all(str(text))
            self._add_asset_to_favorite(parent_item, asset_ids)
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def _add_asset_to_favorite(self, favorite_item, asset_ids):
        """
        将资产添加资产到收藏夹
        :param favorite_item: <QTreeWidgetItem>
        :param asset_ids: <list> list of ids
        :return:
        """
        favorite_item.setExpanded(True)
        favorite = favorite_item.favorite
        with mliber_global.db() as db:
            favorite = db.find_one("Favorite", [["id", "=", favorite.id]])
            exist_assets = favorite.assets
            exist_asset_ids = [asset.id for asset in exist_assets]
            # 当前收藏夹所有的资产id
            new_asset_ids = [asset_id for asset_id in asset_ids if asset_id not in exist_asset_ids]
            if not new_asset_ids:
                return
            new_assets = db.find("Asset", [["id", "in", new_asset_ids]])
            # 将这些新资产加入到store
            all_assets = exist_assets + new_assets
            favorite = db.update("Favorite", favorite.id, {"assets": all_assets})
            favorite_item.set_favorite(favorite)  # 重新设置favorite
            # add to current favorite item
            for asset in new_assets:
                asset_item = FavoriteTreeItem("asset", favorite_item)
                asset_item.set_asset(asset)
            # 发送信号， 在list上显示收藏图标
            self.store_signal.emit()
