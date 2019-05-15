# -*- coding:utf-8 -*-
from Qt.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QAction, QMenu
from Qt.QtCore import Qt
from category_tree import CategoryTree
from mliber_qt_components.search_line_edit import SearchLineEdit
from mliber_qt_components.toolbutton import ToolButton
import mliber_global


class CategoryWidget(QWidget):
    def __init__(self, parent=None):
        super(CategoryWidget, self).__init__(parent)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # top layout
        top_layout = QHBoxLayout()
        # category button
        self.category_btn = QPushButton("Category", self)
        self.category_btn.setFocusPolicy(Qt.NoFocus)
        # refresh button
        self.refresh_btn = ToolButton(self)
        self.refresh_btn.set_size()
        self.refresh_btn.set_icon("refresh.png")
        # search le
        self.search_le = SearchLineEdit(22, 12, self)
        # add button
        top_layout.addWidget(self.category_btn)
        top_layout.addStretch()
        top_layout.addWidget(self.search_le)
        top_layout.addWidget(self.refresh_btn)
        # category tree widget
        self.category_tree = CategoryTree(self)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.category_tree)
        # set signals
        self._set_signals()

    def _set_signals(self):
        """
        信号连接
        :return:
        """
        self.category_btn.clicked.connect(self._show_category_menu)
        self.search_le.text_changed.connect(self._search)
        self.refresh_btn.clicked.connect(self.refresh_ui)

    def refresh_ui(self):
        """
        刷新ui
        :return:
        """
        self.category_tree.refresh_data()
        self.set_completer()

    def set_completer(self):
        """
        set completer
        :return:
        """
        complete_list = self.category_tree.items_mapping.keys()
        self.search_le.set_completer(complete_list)

    def _create_category_menu(self):
        """
        创建setting菜单
        :return:
        """
        menu = QMenu(self)
        user = mliber_global.user()
        if user.category_permission:
            add_category_action = QAction("Add Category", self, triggered=self._add_top_level_category)
            menu.addAction(add_category_action)
        collapse_all_action = QAction("Collapse All", self, triggered=self.collapse_all)
        expand_all_action = QAction("Expand All", self, triggered=self.expand_all)
        menu.addSeparator()
        menu.addAction(collapse_all_action)
        menu.addAction(expand_all_action)
        return menu

    def _show_category_menu(self):
        """
        显示settings菜单
        :return:
        """
        menu = self._create_category_menu()
        point = self.category_btn.rect().bottomLeft()
        point = self.category_btn.mapToGlobal(point)
        menu.exec_(point)

    def collapse_all(self):
        """
        :return:
        """
        self.category_tree.collapseAll()

    def expand_all(self):
        """
        :return:
        """
        self.category_tree.expandAll()

    def _add_top_level_category(self):
        """
        增加顶级的category
        :return:
        """
        self.category_tree.clearSelection()
        self.category_tree.add_category()

    def _search(self, text):
        """
        过滤
        :return:
        """
        self.category_tree.search_item(text)

    def clear(self):
        """
        clear
        :return:
        """
        self.category_tree.clear()
        self.search_le.setText("")
