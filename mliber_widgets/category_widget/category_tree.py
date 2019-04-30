# -*- coding:utf-8 -*-
from PySide.QtGui import QTreeWidget, QTreeWidgetItem, QApplication, QMenu, QAction, QCursor
from PySide.QtCore import Qt
import mliber_global
import mliber_resource
from mliber_qt_components.messagebox import MessageBox


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

    def add_category(self):
        """
        添加category
        :return:
        """
        parent_id = None
        selected_items = self.selected_items()
        if len(selected_items) > 1:
            MessageBox.warning(self, "Warning", "只支持在一个类型下创建子类型")
            return
        if selected_items:
            parent_id = selected_items[0].entity.id
        self.db.create("Category", {"name": "", "parent_id": parent_id})

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
