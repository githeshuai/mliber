# -*- coding:utf-8 -*-
from Qt.QtWidgets import QDialog, QVBoxLayout, QSplitter, QSizePolicy, QListView, QWidget, QStackedLayout
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
        self.category_widget = CategoryWidget(self)
        left_splitter.addWidget(self.category_widget)
        self.tag_widget = TagWidget(self)
        left_splitter.addWidget(self.tag_widget)
        self.splitter.addWidget(left_splitter)
        # middle splitter
        self.middle_splitter = QSplitter(Qt.Vertical, self)
        self.middle_splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        self.asset_widget = AssetWidget(self)
        self.middle_splitter.addWidget(self.asset_widget)
        self.splitter.addWidget(self.middle_splitter)
        # right
        self.right_widget = QWidget(self)
        self.right_widget.setHidden(True)
        self.right_stack = QStackedLayout(self.right_widget)
        self.splitter.addWidget(self.right_widget)
        # splitter settings
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setStretchFactor(2, 0)
        self.splitter.setSizes([250, self.width()-250, 0])
        # add main splitter to main layout
        main_layout.addWidget(self.splitter)
