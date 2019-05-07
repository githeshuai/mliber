# -*- coding:utf-8 -*-
from Qt.QtWidgets import QTreeWidget, QTreeWidgetItem, QApplication, QMenu, QAction, QFrame, QToolButton,\
    QAbstractItemView, QInputDialog, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox
from Qt.QtGui import QCursor
from Qt.QtCore import Qt, Signal
import mliber_global
import mliber_resource
from mliber_qt_components.messagebox import MessageBox
from mliber_libs.os_libs.path import Path


class CategoryTreeItem(QTreeWidgetItem):
    def __init__(self, parent=None):
        super(CategoryTreeItem, self).__init__(parent)
        self.entity = None
        self.father = parent
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
        self.set_signals()

    def set_signals(self):
        """
        信号连接
        :return:
        """
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    @property
    def db(self):
        return mliber_global.app().value("mliber_database")

    @property
    def library(self):
        return mliber_global.app().value("mliber_library")

    @property
    def user(self):
        return mliber_global.app().value("mliber_user")

    def refresh_data(self):
        """
        刷新数据
        :return:
        """
        self.clear()
        cats = self.db.find("Category", [["parent_id", "is", None], ["library_id", "=", self.library.id]])
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

    def selected_items(self):
        """
        获取选中的
        :return:
        """
        selected_items = self.selectedItems()
        return selected_items

    def category_exist(self, category_name, parent_id):
        """
        检查category是否存在
        :param category_name: <str>
        :param parent_id: <int>
        :return:
        """
        parent_id_filters = ["parent_id", "=", parent_id] if parent_id else ["parent_id", "is", None]
        filters = [["name", "=", category_name], ["library_id", "=", self.library.id], parent_id_filters]
        category = self.db.find_one("Category", filters)
        if category:
            return True
        return False

    @staticmethod
    def get_relative_path(category_name, parent_path):
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
        library = mliber_global.app().value("mliber_library")
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
            parent_id = parent_item.entity.id
            parent_path = parent_item.entity.path
        category_exist = self.category_exist(name, parent_id)  # 检查category 是否存在
        if category_exist:
            MessageBox.warning(self, "Warning", u"Category: %s 已存在，不能重复创建." % name)
            return
        # 创建文件夹
        category_relative_path = self.get_relative_path(name, parent_path)
        category_abs_path = self.get_abs_path(category_relative_path)
        try:
            Path(category_abs_path).makedirs()
        except WindowsError as e:
            MessageBox.critical(self, "Window Error", str(e))
            return
        # 在数据库里添加
        category = self.db.create("Category", {"name": name, "parent_id": parent_id, "path": category_relative_path,
                                               "user_id": self.user.id, "library_id": self.library.id})
        # 在ui上显示
        tree_widget_item = CategoryTreeItem(parent_item or self)
        tree_widget_item.set_entity(category)
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
            relative_path = selected_items[0].entity.path
            path = self.get_abs_path(relative_path)
        else:
            path = self.library.root_path()
        Path(path).open()

    def recursion_delete_category(self, category):
        """
        递归删除子类型
        :param category: Category instance
        :return:
        """
        self.db.delete(category)
        children = self.db.find("Category", [["parent_id", "=", category.id]])
        if children:
            for child in children:
                self.recursion_delete_category(child)

    def delete_category(self):
        """
        删除category之前
        :return:
        """
        selected_items = self.selected_items()
        if not selected_items:
            return
        if not self.user.category_permission:
            MessageBox.warning(self, "Warning", u"你没有权限执行此操作")
            return
        else:
            dialog = DeleteCategoryDialog(self)
            dialog.accept_signal.connect(self._delete_category)
            dialog.exec_()

    def _delete_category(self, delete_source_file):
        """
        删除category
        :return:
        """
        selected_items = self.selected_items()
        selected_item = selected_items[0]
        category_relative_path = selected_item.entity.path
        category_abs_path = self.get_abs_path(category_relative_path)
        # 先删除数据库记录, 如果有子类别一并删除
        self.recursion_delete_category(selected_item.entity)
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
                print str(e)
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


class DeleteCategoryDialog(QDialog):
    accept_signal = Signal(bool)

    def __init__(self, parent=None):
        super(DeleteCategoryDialog, self).__init__(parent)
        self.resize(300, 180)
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(20)
        self.setWindowTitle("Delete Category")
        self.text_label = QLabel(self)
        self.text_label.setFixedHeight(20)
        self.text_label.setText(u"请输入密码")
        self.password_le = QLineEdit(self)
        self.password_le.setEchoMode(QLineEdit.Password)
        # layout include checkbox and info label
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)
        self.check = QCheckBox(u"同时删除源文件", self)
        self.info_label = QToolButton(self)
        self.info_label.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.info_label.setStyleSheet("border: 0px; padding: 0px; background: transparent;"
                                      "color: #F00; font: bold; font-size: 12px; height: 22px; font-family: Arial")
        self.info_label.setHidden(True)
        layout.addWidget(self.check)
        layout.addStretch()
        layout.addWidget(self.info_label)
        # button layout
        button_layout = QHBoxLayout()
        self.ok_btn = QPushButton("Ok", self)
        self.close_btn = QPushButton("Cancel", self)
        button_layout.addStretch()
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.close_btn)
        # add to main layout
        main_layout.addWidget(self.text_label)
        main_layout.addWidget(self.password_le)
        main_layout.addLayout(layout)
        main_layout.addLayout(button_layout)
        # set signals
        self.set_signals()

    def set_signals(self):
        """
        信号连接
        :return:
        """
        self.ok_btn.clicked.connect(self.on_ok_button_clicked)
        self.close_btn.clicked.connect(self._close)

    @property
    def password(self):
        """
        密码
        :return:
        """
        return self.password_le.text()

    @property
    def delete_source(self):
        """
        是否删除源文件
        :return: <bool>
        """
        return self.check.isChecked()

    def _login_failed(self):
        """
        show error information
        Returns:
        """
        self.info_label.setHidden(False)
        self.info_label.setIcon(mliber_resource.icon("error.png"))
        self.info_label.setText(u"密码错误！")

    def validate_password(self):
        """
        检查密码是否正确
        :return:
        """
        user = mliber_global.app().value("mliber_user")
        password = user.password
        if self.password == password:
            return True
        return False

    def on_ok_button_clicked(self):
        """
        当ok按钮按下的时候
        :return:
        """
        if self.validate_password():
            self.accept_signal.emit(self.delete_source)
            self._close()
        else:
            self._login_failed()
            
    def _close(self):
        """
        
        :return: 
        """
        self.close()
        self.deleteLater()


if __name__ == "__main__":
    app = QApplication([])
    ct = DeleteCategoryDialog()
    ct.show()
    app.exec_()
