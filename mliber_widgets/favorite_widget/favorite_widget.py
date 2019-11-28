#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date      : 2019-11-26 16:07
# Author    : Mr. He
# Version   :
# Usage     : 
# Notes     :

# Import built-in modules

# Import third-party modules
from Qt.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QMenu, QAction
# Import local modules
from mliber_widgets.favorite_widget.favorite_tree import FavoriteTree
import mliber_global
from mliber_qt_components.toolbutton import ToolButton
from mliber_qt_components.search_line_edit import SearchLineEdit
from mliber_qt_components.indicator_button import IndicatorButton


class FavoriteWidget(QWidget):
    def __init__(self, parent=None):
        super(FavoriteWidget, self).__init__(parent)
        self._setup_ui()
        self._set_signals()
        self.refresh_ui()

    def _setup_ui(self):
        """
        setup ui
        :return:
        """
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # top layout
        top_layout = QHBoxLayout()
        # category button
        self.favorite_btn = IndicatorButton("Favorite", self)
        # refresh button
        self.refresh_btn = ToolButton(self)
        self.refresh_btn.set_size(25, 25)
        self.refresh_btn.set_icon("refresh.png")
        # search le
        self.search_le = SearchLineEdit(22, 12, self)
        # add button
        top_layout.addWidget(self.favorite_btn)
        top_layout.addStretch()
        top_layout.addWidget(self.search_le)
        top_layout.addWidget(self.refresh_btn)
        # category tree widget
        self.favorite_tree = FavoriteTree(self)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.favorite_tree)

    def _set_signals(self):
        """
        :return:
        """
        self.favorite_btn.clicked.connect(self._show_favorite_menu)
        self.search_le.text_changed.connect(self._search)
        self.refresh_btn.clicked.connect(self.refresh_ui)

    def _create_favorite_menu(self):
        """
        创建setting菜单
        :return:
        """
        menu = QMenu(self)
        add_favorite_action = QAction("Add Category", self, triggered=self._add_favorite)
        menu.addAction(add_favorite_action)
        collapse_all_action = QAction("Collapse All", self, triggered=self.collapse_all)
        expand_all_action = QAction("Expand All", self, triggered=self.expand_all)
        menu.addSeparator()
        menu.addAction(collapse_all_action)
        menu.addAction(expand_all_action)
        return menu

    def _show_favorite_menu(self):
        """
        显示settings菜单
        :return:
        """
        menu = self._create_favorite_menu()
        point = self.favorite_btn.rect().bottomLeft()
        point = self.favorite_btn.mapToGlobal(point)
        menu.exec_(point)

    def _add_favorite(self):
        """
        add favorite
        :return: 
        """
        self.favorite_tree.add_favorite()
        
    def refresh_ui(self):
        """
        刷新ui
        :return:
        """
        self.favorite_tree.refresh_data()
        self.set_completer()

    def set_completer(self):
        """
        set completer
        :return:
        """
        complete_list = self.favorite_tree.items_mapping.keys()
        self.search_le.set_completer(complete_list)

    def _search(self, text):
        """
        过滤
        :return:
        """
        self.favorite_tree.search_item(text)

    def clear(self):
        """
        clear
        :return:
        """
        self.favorite_tree.clear()
        self.search_le.setText("")
    
    def collapse_all(self):
        """
        :return:
        """
        self.favorite_tree.collapseAll()

    def expand_all(self):
        """
        :return:
        """
        self.favorite_tree.expandAll()

    def deselect_all(self):
        """
        清空选择
        :return:
        """
        self.favorite_tree.clearSelection()
