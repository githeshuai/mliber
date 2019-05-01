# -*- coding:utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtGui import *
from Qt.QtCore import *
from library_list_view import LibraryListView
import mliber_resource
from mliber_qt_components.search_line_edit import SearchLineEdit
from mliber_conf.library_type import LIBRARY_TYPE


class LibraryManage(QDialog):
    def __init__(self, parent=None):
        super(LibraryManage, self).__init__(parent)
        # setup ui
        self.resize(630, 500)
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # search layout
        search_frame = QFrame(self)
        search_frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(0, 2, 0, 2)
        search_layout.addStretch()
        self.search_btngrp = QButtonGroup()
        self.name_check_box = QCheckBox("name", self)
        self.name_check_box.setChecked(True)
        self.type_check_box = QCheckBox("type", self)
        self.search_btngrp.addButton(self.name_check_box)
        self.search_btngrp.addButton(self.type_check_box)
        search_layout.addWidget(self.name_check_box)
        search_layout.addWidget(self.type_check_box)
        search_layout.setSpacing(10)
        # search stacked
        self.search_stacked_widget = QStackedWidget(self)
        self.type_combo = QComboBox(self)
        self.search_le = SearchLineEdit(22, 12, self)
        self.search_stacked_widget.addWidget(self.search_le)
        self.search_stacked_widget.addWidget(self.type_combo)
        # add to search layout
        search_layout.addWidget(self.search_stacked_widget)
        # library list view
        self.library_list_view = LibraryListView(self)
        # button layout

        # add to main layout
        main_layout.addWidget(search_frame)
        main_layout.addWidget(self.library_list_view)
        main_layout.setStretch(0, 0)
        main_layout.setStretch(1, 1)
        # set style
        self.set_style()
        # set signals
        self._set_signals()
        # init
        self.init()

    def set_style(self):
        """
        set style
        :return:
        """
        self.setStyleSheet(mliber_resource.style())

    def init(self):
        """
        initialize
        :return:
        """
        library_names = self.library_list_view.library_names()
        self.search_le.set_completer(library_names)
        self.type_combo.addItems(LIBRARY_TYPE)

    def _set_signals(self):
        """
        信号链接
        :return:
        """
        self.search_btngrp.buttonClicked.connect(self.switch_search_type)
        self.search_le.return_pressed.connect(self._filter)
        self.type_combo.currentIndexChanged.connect(self._filter)

    def switch_search_type(self, button):
        """
        切换搜索类型
        :return:
        """
        if button is self.name_check_box:
            self.search_stacked_widget.setCurrentIndex(0)
            self._set_filter_type("name")
        else:
            self.search_stacked_widget.setCurrentIndex(1)
            self._set_filter_type("type")

    def _set_filter_type(self, typ):
        """
        设置过滤类型， name or type
        :param typ: <str>
        :return:
        """
        self.library_list_view.model().set_filter_type(typ)

    @property
    def filter_value(self):
        """
        获取过滤值
        :return:
        """
        if self.search_stacked_widget.currentIndex() == 0:
            return self.search_le.text()
        return self.type_combo.currentText()

    def _filter(self):
        """
        过滤
        :return:
        """
        self.library_list_view.model().set_filter(self.filter_value)
        self.library_list_view.show_delegate()
