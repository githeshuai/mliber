# -*- coding:utf-8 -*-
from Qt.QtWidgets import QTreeWidget, QTreeWidgetItem, QApplication, QMenu, QAction, QFrame, \
    QAbstractItemView, QInputDialog
from Qt.QtGui import QCursor
from Qt.QtCore import Qt
import mliber_global
import mliber_resource
from mliber_qt_components.messagebox import MessageBox
from mliber_libs.os_libs.path import Path


class CategoryTreeItem(QTreeWidgetItem):
    def __init__(self, parent=None):
        super(CategoryTreeItem, self).__init__(parent)
        self.entity = None
        self.setIcon(0, mliber_resource.icon("category.png"))

    def set_entity(self, entity):
        """
        :param entity: 表对象
        :return:
        """
        self.entity = entity
        self.setText(0, entity.name)


class CategoryTree(QTreeWidget):
    def __init__(self, parent=None):
        super(CategoryTree, self).__init__(parent)
        self.setSelectionMode(self.ExtendedSelection)
        self.setFocusPolicy(Qt.NoFocus)
        self.setHeaderHidden(True)
        self.setFrameShape(QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.items_mapping = {}
        self.app = None
        self.set_signals()

    def set_signals(self):
        """
        信号连接
        :return:
        """
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def refresh_global(self):
        """
        刷新global
        :return:
        """
        self.app = mliber_global.app()
        self.db = self.app.value("mliber_database")
        self.library = self.app.value("mliber_library")
        self.user = self.app.value("mliber_user")

    def refresh_data(self):
        """
        刷新数据
        :return:
        """
        self.clear()
        cats = self.db.find("Category", [["parent_id", "is", None]])
        for cat in cats:
            cat_item = CategoryTreeItem(self)
            cat_item.set_entity(cat)
            self.items_mapping[cat.name] = cat_item
            self.get_children(cat, cat_item)

    def get_children(self, cat, parent_item):
        """
        递归获取子类型
        :param cat: Category对象
        :param parent_item: <QTreeWidgetItem>
        :return:
        """
        cat_id = cat.id
        children = self.db.find("Category", [["parent_id", "=", cat_id]])
        if not children:
            return
        for child in children:
            child_item = CategoryTreeItem(parent_item)
            child_item.set_entity(child)
            self.items_mapping[child.name] = child_item
            self.get_children(child, child_item)

    def show_context_menu(self):
        """
        显示右键菜单
        :return:
        """
        menu = QMenu(self)
        show_in_explore_action = QAction(u"打开路径", self, triggered=self.open_category)
        add_category_action = QAction(u"添加子类型", self, triggered=self.add_category)
        delete_action = QAction(u"删除", self, triggered=self.delete_category)
        menu.addAction(show_in_explore_action)
        menu.addAction(add_category_action)
        menu.addAction(delete_action)
        menu.exec_(QCursor.pos())

    def open_category(self):
        """
        show in explore
        :return:
        """
        pass

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
        library = mliber_global.app().value("mliber_library")
        if not library:
            MessageBox.warning(self, "Warning", u"请先选择library")
            return False
        return True

    def category_exist(self, category_name, parent_id):
        """
        检查category是否存在
        :param category_name: <str>
        :param parent_id: <int>
        :return:
        """
        parent_id_filters = ["parent_id", "=", parent_id] if parent_id else ["parent_id", "is", None]
        filters = [["name", "=", category_name], parent_id_filters]
        category = self.db.find_one("Category", filters)
        if category:
            return True
        return False

    @staticmethod
    def get_category_dir(category_name, parent_path):
        """
        创建category路径
        :param category_name: <str>
        :param parent_path: <str>
        :return:
        """
        if not parent_path:
            library_path = mliber_global.app().value("mliber_library").root_path()
            category_dir = Path(library_path).join(category_name)
        else:
            category_dir = Path(parent_path).join(category_name)
        return category_dir

    def add_category(self):
        """
        添加category
        :return:
        """
        if not self.pre_add_category():
            return
        parent_id = None
        parent_path = None
        selected_items = self.selected_items()
        if selected_items:
            parent_id = selected_items[0].entity.id
            parent_path = selected_items[0].entity.path
        name, ok = QInputDialog.getText(self, "Add Category", "Category Name")
        #  检查category 是否存在
        if name and ok:
            category_exist = self.category_exist(name, parent_id)
            if category_exist:
                MessageBox.warning(self, "Warning", u"Category: %s 已存在，不能重复创建." % name)
                return
            # 创建文件夹
            category_dir = self.get_category_dir(name, parent_path)
            try:
                Path(category_dir).makedirs()
            except WindowsError as e:
                MessageBox.critical(self, "Window Error", str(e))
                return
        # 然后在数据库里添加
            category = self.db.create("Category", {"name": name, "parent_id": parent_id, "path": category_dir,
                                                   "user_id": self.user.id, "library_id": self.library.id})
        self.refresh_data()

    def delete_category(self):
        """
        删除category
        :return:
        """
        return

    def selected_items(self):
        """
        获取选中的
        :return:
        """
        selected_items = self.selectedItems()
        return selected_items


if __name__ == "__main__":
    app = QApplication([])
    ct = CategoryTree()
    ct.refresh_global()
    # ct.set_root("D:/asset_library")
    ct.refresh_data()
    ct.show()
    app.exec_()
