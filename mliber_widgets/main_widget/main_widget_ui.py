# -*- coding:utf-8 -*-
from Qt.QtWidgets import QDialog, QVBoxLayout, QSplitter, QSizePolicy, QListView, QWidget, QStackedLayout, QSizeGrip
from Qt.QtCore import Qt
from mliber_widgets.toolbar import Toolbar
from mliber_widgets.category_widget import CategoryWidget
from mliber_widgets.tag_widget import TagWidget
from mliber_widgets.asset_widget import AssetWidget
from mliber_widgets.statusbar import StatusBar


class MainWidgetUI(QDialog):
    def __init__(self, parent=None):
        super(MainWidgetUI, self).__init__(parent)
        self.resize(1120, 900)
        self.setWindowFlags(Qt.Window)
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # tool bar
        self.tool_bar = Toolbar(self)
        main_layout.addWidget(self.tool_bar)
        # main splitter
        self.splitter = QSplitter(Qt.Horizontal, self)
        self.splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        self.splitter.setHandleWidth(2)
        self.splitter.setChildrenCollapsible(False)

        # left splitter
        self.left_splitter = QSplitter(Qt.Vertical, self)
        self.left_splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        self.left_splitter.setHandleWidth(2)
        self.left_splitter.setChildrenCollapsible(False)
        self.category_widget = CategoryWidget(self)
        self.left_splitter.addWidget(self.category_widget)
        self.tag_widget = TagWidget(self)
        self.left_splitter.addWidget(self.tag_widget)
        # middle splitter
        self.middle_splitter = QSplitter(Qt.Vertical, self)
        self.middle_splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        self.asset_widget = AssetWidget(self)
        self.middle_splitter.addWidget(self.asset_widget)
        # right
        self.right_widget = QWidget(self)
        self.right_widget.setHidden(True)
        self.right_stack = QStackedLayout(self.right_widget)
        # add to main splitter
        self.splitter.addWidget(self.left_splitter)
        self.splitter.addWidget(self.middle_splitter)
        self.splitter.addWidget(self.right_widget)
        # splitter settings
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setStretchFactor(2, 0)
        self.splitter.setSizes([250, self.width()-250, 0])
        # add main splitter to main layout
        main_layout.addWidget(self.splitter)
        # add status bar
        self.status_bar = StatusBar(self)
        self.status_bar.clear()
        main_layout.addWidget(self.status_bar)
        main_layout.setSpacing(0)
        # size grip
        size_grip = QSizeGrip(self)
        main_layout.addWidget(size_grip, 0, Qt.AlignBottom | Qt.AlignRight)
        main_layout.setSpacing(0)
