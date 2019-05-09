# -*- coding:utf-8 -*-
from Qt.QtWidgets import QDialog, QVBoxLayout, QSplitter, QSizePolicy, QListView
from Qt.QtCore import Qt
from mliber_widgets.toolbar import Toolbar
from mliber_widgets.category_widget import CategoryWidget
from mliber_widgets.tag_widget import TagWidget
from mliber_widgets.asset_widget import AssetWidget


class MainWidgetUI(QDialog):
    def __init__(self, parent=None):
        super(MainWidgetUI, self).__init__(parent)
        self.resize(1000, 800)
        self.setWindowFlags(Qt.Window)
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        # tool bar
        self.tool_bar = Toolbar(self)
        main_layout.addWidget(self.tool_bar)
        # main splitter
        self.splitter = QSplitter(Qt.Horizontal, self)
        self.splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        self.splitter.setHandleWidth(2)
        self.splitter.setChildrenCollapsible(False)
        # left splitter
        left_splitter = QSplitter(Qt.Vertical, self)
        left_splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        left_splitter.setHandleWidth(2)
        left_splitter.setChildrenCollapsible(False)
        # add category widget to left splitter
        self.category_widget = CategoryWidget(self)
        left_splitter.addWidget(self.category_widget)
        # add tag widget to left splitter
        self.tag_widget = TagWidget(self)
        left_splitter.addWidget(self.tag_widget)
        # add left splitter to main splitter
        self.splitter.addWidget(left_splitter)
        # add asset list view to main splitter
        self.asset_widget = AssetWidget(self)
        self.splitter.addWidget(self.asset_widget)
        # add main splitter to main layout
        main_layout.addWidget(self.splitter)
