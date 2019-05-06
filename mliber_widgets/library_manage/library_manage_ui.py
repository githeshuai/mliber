# -*- coding: utf-8 -*-
from Qt.QtWidgets import QDialog, QVBoxLayout, QFrame, QHBoxLayout, QButtonGroup, QCheckBox, QStackedWidget, QComboBox
from Qt.QtCore import Qt
from library_list_view import LibraryListView
from mliber_qt_components.search_line_edit import SearchLineEdit
from mliber_qt_components.toolbutton import ToolButton


class LibraryManageUI(QDialog):
    def __init__(self, parent=None):
        super(LibraryManageUI, self).__init__(parent)
        self.setWindowTitle("Library Manager")
        # setup ui
        self.resize(650, 550)
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # search layout
        search_frame = QFrame(self)
        search_frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        top_layout = QHBoxLayout(search_frame)
        top_layout.setContentsMargins(0, 5, 0, 2)
        # toolbar
        self.menu_bar = ToolButton(self)
        self.menu_bar.set_size(28, 28)
        self.menu_bar.set_icon("category.png")
        top_layout.addWidget(self.menu_bar)
        # search
        top_layout.addStretch()
        self.search_btngrp = QButtonGroup()
        self.name_check_box = QCheckBox("name", self)
        self.name_check_box.setChecked(True)
        self.type_check_box = QCheckBox("type", self)
        self.search_btngrp.addButton(self.name_check_box)
        self.search_btngrp.addButton(self.type_check_box)
        top_layout.addWidget(self.name_check_box)
        top_layout.addWidget(self.type_check_box)
        top_layout.setSpacing(10)
        # search stacked
        self.search_stacked_widget = QStackedWidget(self)
        self.type_combo = QComboBox(self)
        self.type_combo.setMaximumHeight(25)
        self.search_le = SearchLineEdit(25, 12, self)
        self.search_stacked_widget.addWidget(self.search_le)
        self.search_stacked_widget.addWidget(self.type_combo)
        # add to search layout
        top_layout.addWidget(self.search_stacked_widget)
        # refresh button
        self.refresh_btn = ToolButton(self)
        self.refresh_btn.set_size(28, 28)
        self.refresh_btn.set_icon("refresh.png")
        top_layout.addWidget(self.refresh_btn)
        # library list view
        self.library_list_view = LibraryListView(self)
        # add to main layout
        main_layout.addWidget(search_frame)
        main_layout.addWidget(self.library_list_view)
        main_layout.setStretch(0, 0)
        main_layout.setStretch(1, 1)
