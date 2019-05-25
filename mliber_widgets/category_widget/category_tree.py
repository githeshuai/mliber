# -*- coding:utf-8 -*-
import logging
from datetime import datetime
from Qt.QtWidgets import QTreeWidget, QTreeWidgetItem, QApplication, QMenu, QAction, QFrame, QToolButton,\
    QAbstractItemView, QInputDialog, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox
from Qt.QtGui import QCursor
from Qt.QtCore import Qt, Signal
import mliber_global
import mliber_resource
from mliber_qt_components.messagebox import MessageBox
from mliber_libs.os_libs.path import Path
from mliber_qt_components.delete_widget import DeleteWidget


class CategoryTreeItem(QTreeWidgetItem):
    def __init__(self, parent=None):
        super(CategoryTreeItem, self).__init__(parent)
        self.category = None
        self.father = parent
        self.setIcon(0, mliber_resource.icon("category.png"))

    def set_category(self, category):
        """
        :param category: 表对象
        :return:
        """
        self.category = category
        self.setText(0, category.name)
        library = mliber_global.library()
        path = category.path.format(root=library.root_path())
        tooltip_str = "id: %s \npath: %s" % (str(category.id), path)
        self.setToolTip(0, tooltip_str)


class CategoryTree(QTreeWidget):
    selection_changed = Signal(list)
    deleted_signal = Signal()

    def __init__(self, parent=None):
        super(CategoryTree, self).__init__(parent)
        self.setSelectionMode(self.ExtendedSelection)
        self.setFocusPolicy(Qt.NoFocus)
        self.setHeaderHidden(True)
        self.setFrameShape(QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.items_mapping = {}
        self._set_signals()

    def _set_signals(self):
        """
        信号连接
        :return:
        """
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
        self.itemPressed.connect(self._on_item_selection_changed)

    @property
    def library(self):
        return mliber_global.library()

    @property
    def user(self):
        return mliber_global.user()

    def refresh_data(self):
        """
        刷新数据
        :return:
        """
        self.clear()
        if not self.library:
            return
        with mliber_global.db() as db:
            cats = db.find("Category", [["parent_id", "is", None],
                                        ["library_id", "=", self.library.id],
                                        ["status", "=", "Active"]])
            for cat in cats:
                cat_item = CategoryTreeItem(self)
                cat_item.set_category(cat)
                self.items_mapping[cat.name] = cat_item
                self._create_children_item(cat, cat_item)

    def _create_children_item(self, cat, parent_item):
        """
        递归获取子类型
        :param cat: Category对象
        :param parent_item: <QTreeWidgetItem>
        :return:
        """
        cat_id = cat.id
        with mliber_global.db() as db:
            children = db.find("Category", [["parent_id", "=", cat_id], ["status", "=", "Active"]])
            if not children:
                return
            for child in children:
                child_item = CategoryTreeItem(parent_item)
                child_item.set_category(child)
                self.items_mapping[child.name] = child_item
                self._create_children_item(child, child_item)

    def _show_context_menu(self):
        """
        显示右键菜单
        :return:
        """
        menu = QMenu(self)
        show_in_explore_action = QAction("Open in Explorer", self, triggered=self.open_category)
        menu.addAction(show_in_explore_action)
        if self.user.category_permission:
            add_category_action = QAction("Add Category", self, triggered=self.add_category)
            delete_action = QAction(mliber_resource.icon("delete.png"), u"Send to Trash", self,
                                    triggered=self.delete_category)
            menu.addAction(add_category_action)
            menu.addSeparator()
            menu.addAction(delete_action)
        menu.exec_(QCursor.pos())

    def selected_items(self):
        """
        获取选中的item
        :return:
        """
        selected_items = self.selectedItems()
        return selected_items

    def selected_categories(self):
        """
        获取选中的category
        :return:
        """
        selected_items = self.selected_items()
        categories = [item.category for item in selected_items]
        return categories

    def _on_item_selection_changed(self):
        """
        当item 选择改变的时候
        :return:
        """
        selected_categories = self.selected_categories()
        mliber_global.app().set_value(mliber_categories=selected_categories)
        categories = self._get_children_categories(selected_categories)
        self.selection_changed.emit(categories)

    def _category_exist(self, category_name, parent_id):
        """
        检查category是否存在
        :param category_name: <str>
        :param parent_id: <int>
        :return:
        """
        parent_id_filters = ["parent_id", "=", parent_id] if parent_id else ["parent_id", "is", None]
        filters = [["name", "=", category_name], ["library_id", "=", self.library.id], parent_id_filters]
        with mliber_global.db() as db:
            category = db.find_one("Category", filters)
        if category:
            return True
        return False

    @staticmethod
    def _get_relative_path(category_name, parent_path):
        """
        创建category相对路径路径
        :param category_name: <str>
        :param parent_path: <str>
        :return: 相对路径{root}/category_name/.....
        """
        if not parent_path:
            category_dir = "{root}/%s" % category_name
        else:
            category_dir = "%s/%s" % (parent_path, category_name)
        return category_dir

    def get_abs_path(self, relative_path):
        """
        获取绝对路径
        :param relative_path: <str> 相对路径 {root}/...
        :return:
        """
        root_path = self.library.root_path()
        return relative_path.format(root=root_path)

    def pre_add_category(self):
        """
        在创建category之前需要做的准备
        :return:
        """
        # 检查是否选择了多个category
        selected_items = self.selected_items()
        if len(selected_items) > 1:
            MessageBox.warning(self, "Warning", "只支持在一个类型下创建子类型")
            return False
        # 检查是否选择了library
        library = self.library
        if not library:
            MessageBox.warning(self, "Warning", u"请先选择library")
            return False
        return True

    def add_category(self):
        """
        添加category
        :return:
        """
        if not self.pre_add_category():
            return
        selected_item = None
        selected_items = self.selected_items()
        if selected_items:
            selected_item = selected_items[0]
        name, ok = QInputDialog.getText(self, "Add Category", "Category Name")
        if name and ok:
            self._add_category(name, selected_item)

    def _add_category(self, name, parent_item):
        """
        :param name: <str>
        :param parent_item: <QTreeWidgetItem or QTreeWidget>
        :return:
        """
        parent_id = None
        parent_path = None
        if isinstance(parent_item, QTreeWidgetItem):
            parent_id = parent_item.category.id
            parent_path = parent_item.category.path
        category_exist = self._category_exist(name, parent_id)  # 检查category 是否存在
        if category_exist:
            MessageBox.warning(self, "Warning", u"Category: %s 已存在，不能重复创建." % name)
            return
        # 创建文件夹
        category_relative_path = self._get_relative_path(name, parent_path)
        category_abs_path = self.get_abs_path(category_relative_path)
        try:
            Path(category_abs_path).makedirs()
        except WindowsError as e:
            MessageBox.critical(self, "Window Error", str(e))
            return
        # 在数据库里添加
        with mliber_global.db() as db:
            category = db.create("Category", {"name": name, "parent_id": parent_id, "path": category_relative_path,
                                              "created_by": self.user.id, "library_id": self.library.id})
        # 在ui上显示
        tree_widget_item = CategoryTreeItem(parent_item or self)
        tree_widget_item.set_category(category)
        self.items_mapping[name] = tree_widget_item
        if parent_item:
            parent_item.setExpanded(True)

    def open_category(self):
        """
        show in explore
        :return:
        """
        selected_items = self.selected_items()
        if selected_items:
            relative_path = selected_items[0].category.path
            path = self.get_abs_path(relative_path)
        else:
            path = self.library.root_path()
        Path(path).open()
        
    @staticmethod
    def _get_children_categories(categories):
        """
        获取子类型，需要递归
        :param categories: <list> list of Category
        :return:
        """
        all_categories = list()

        def get(category_list):
            category_id_list = [category.id for category in category_list]
            with mliber_global.db() as db:
                children_categories = db.find("Category", 
                                              [["parent_id", "in", category_id_list], 
                                               ["status", "=", "Active"]])
                if children_categories:
                    all_categories.extend(children_categories)
                    get(children_categories)
        get(categories)
        all_categories.extend(categories)
        return all_categories
    
    def _recursion_delete_category(self, category):
        """
        递归删除子类型
        :param category: Category instance
        :return:
        """
        categories = self._get_children_categories([category])
        category_ids = [category.id for category in categories]
        with mliber_global.db() as db:
            for category in categories:
                db.update("Category", category.id, {"status": "Disable", "updated_by": self.user.id,
                                                    "updated_at": datetime.now()})
            assets = db.find("Asset", [["category_id", "in", category_ids], ["status", "=", "Active"]])
            for asset in assets:
                db.update("Asset", asset.id, {"status": "Disable", "updated_by": self.user.id,
                                              "updated_at": datetime.now()})
        
    def delete_category(self):
        """
        删除category之前
        :return:
        """
        selected_items = self.selected_items()
        if not selected_items:
            return
        dialog = DeleteWidget(self)
        dialog.accept_signal.connect(self._delete_category)
        dialog.exec_()

    def _delete_category(self, delete_source_file):
        """
        删除category
        :return:
        """
        selected_items = self.selected_items()
        selected_item = selected_items[0]
        category_relative_path = selected_item.category.path
        category_abs_path = self.get_abs_path(category_relative_path)
        # 先删除数据库记录, 如果有子类别一并删除, 并且删除资产
        self._recursion_delete_category(selected_item.category)
        # 从tree widget中移除
        parent = selected_item.father
        if parent is self:
            index = self.indexOfTopLevelItem(selected_item)
            self.takeTopLevelItem(index)
        else:
            parent.removeChild(selected_item)
            del selected_item
        # 删除源文件
        if delete_source_file:
            try:
                Path(category_abs_path).remove()
            except WindowsError as e:
                logging.error(str(e))
                MessageBox.warning(self, "Warning", u"源文件删除失败，请手动删除")

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
