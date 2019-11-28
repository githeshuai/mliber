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

    def add_asset(self, asset_name):
        """
        :param asset_name: <str>
        :return:
        """
        child_item = FavoriteTreeItem("asset", self)
        child_item.setText(0, asset_name)


class FavoriteTree(QTreeWidget):
    selection_changed = Signal(list)
    deleted_signal = Signal()

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
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
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
        favorites = [item.favorite for item in selected_items]
        return favorites

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
            for favorite in favorites:
                favorite_item = FavoriteTreeItem(parent=self)
                favorite_item.set_favorite(favorite)
                self.items_mapping[favorite.name] = favorite_item
                items.append(favorite_item)
                id_item_mapping[favorite.id] = favorite_item

            for item in items:
                parent_id = item.favorite.parent_id
                if parent_id:
                    index = self.indexOfTopLevelItem(item)
                    self.takeTopLevelItem(index)
                    id_item_mapping.get(parent_id).addChild(item)

    def _show_context_menu(self):
        """
        显示右键菜单
        :return:
        """
        menu = QMenu(self)
        add_favorite_action = QAction("Add Favorite", self, triggered=self.add_favorite)
        delete_action = QAction(mliber_resource.icon("delete.png"), u"Send to Trash", self,
                                triggered=self.delete_favorite)
        menu.addAction(add_favorite_action)
        menu.addSeparator()
        menu.addAction(delete_action)
        menu.exec_(QCursor.pos())

    def delete_favorite(self):
        """
        delete favorite
        :return:
        """
        selected_items = self.selected_items()
        selected_item = selected_items[0]
        self.recursion_delete_favorite(selected_item.favorite)
        # 从tree widget中移除
        parent = selected_item.father
        if parent is self:
            index = self.indexOfTopLevelItem(selected_item)
            self.takeTopLevelItem(index)
        else:
            parent.removeChild(selected_item)
            del selected_item

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
        selected_favorites = self.selected_favorites()
        favorites = self._get_children_favorites(selected_favorites)
        self.selection_changed.emit(favorites)

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
            items = yaml.load_all(str(text))
            for item in items:
                asset_id, asset_name = item
                parent_item.add_asset(asset_name)
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
