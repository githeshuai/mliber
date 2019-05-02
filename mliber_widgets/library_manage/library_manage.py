# -*- coding:utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtGui import *
from Qt.QtCore import *
import mliber_resource
import mliber_global
from mliber_conf.library_type import LIBRARY_TYPE
from library_manage_ui import LibraryManageUI
from mliber_qt_components.path_widget import PathWidget
from mliber_qt_components.choose_path_widget import ChoosePathWidget


class CreateLibraryWidget(QDialog):
    create = Signal(list)

    def __init__(self, parent=None):
        super(CreateLibraryWidget, self).__init__(parent)
        main_layout = QVBoxLayout(self)
        # name layout
        name_layout = QHBoxLayout()
        name_label = QLabel("name", self)
        self.name_le = QLineEdit(self)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_le)
        # type layout
        type_layout = QHBoxLayout()
        type_label = QLabel("type", self)
        type_label.setMaximumWidth(30)
        self.type_combo = QComboBox(self)
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)
        # path widget
        self.path_widget = PathWidget(self)
        self.choose_path_widget = ChoosePathWidget(self)
        self.choose_path_widget.set_label_text(u"图标")
        # description
        description_layout = QHBoxLayout()
        description_label = QLabel(u"描述", self)
        description_label.setAlignment(Qt.AlignTop)
        self.description_te = QTextEdit(self)
        description_layout.addWidget(description_label)
        description_layout.addWidget(self.description_te)
        # button layout
        button_layout = QHBoxLayout()
        self.create_btn = QPushButton("Create")
        self.close_btn = QPushButton("Close")
        button_layout.addStretch()
        button_layout.addWidget(self.create_btn)
        button_layout.addWidget(self.close_btn)
        # add to main layout
        main_layout.addLayout(name_layout)
        main_layout.addLayout(type_layout)
        main_layout.addWidget(self.path_widget)
        main_layout.addWidget(self.choose_path_widget)
        main_layout.addLayout(description_layout)
        main_layout.addLayout(button_layout)
        # init
        self.init()
        # set signals
        self.set_signals()

    def init(self):
        """
        initialize
        :return:
        """
        self.type_combo.addItems(LIBRARY_TYPE)

    def set_signals(self):
        """
        :return:
        """
        self.create_btn.clicked.connect(self.on_create_btn_clicked)
        self.close_btn.clicked.connect(self.close)

    @property
    def name(self):
        """
        :return:<str>
        """
        return self.name_le.text()

    @property
    def type(self):
        """
        :return: <str>
        """
        return self.type_combo.currentText()

    @property
    def windows_path(self):
        """
        windows path
        :return:
        """
        return self.path_widget.windows_path()

    @property
    def linux_path(self):
        """
        linux path
        :return:
        """
        return self.path_widget.linux_path()

    @property
    def mac_path(self):
        """
        mac path
        :return:
        """
        return self.path_widget.mac_path()

    @property
    def icon_path(self):
        """
        mac path
        :return:
        """
        return self.choose_path_widget.path

    @property
    def description(self):
        """
        :return: <str>
        """
        return self.description_te.toPlainText()

    def on_create_btn_clicked(self):
        """
        当create button click
        :return:
        """
        self.create.emit([self.name, self.type, self.windows_path, self.linux_path, self.mac_path,
                          self.icon_path, self.description])
        self.accept()


class LibraryManage(LibraryManageUI):
    def __init__(self, parent=None):
        super(LibraryManage, self).__init__(parent)
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
        self.menu_bar.clicked.connect(self.add_menu)

    def add_menu(self):
        """
        menu bar add menu
        :return:
        """
        menu = QMenu(self)
        app = mliber_global.app()
        user = app.value("mliber_user")
        if user.library_permission:
            add_action = QAction("Add", self, triggered=self.show_create_library_widget)
            menu.addAction(add_action)
        exit_action = QAction("exit", self, triggered=self.close)
        menu.addAction(exit_action)
        point = self.menu_bar.rect().bottomLeft()
        point = self.menu_bar.mapToGlobal(point)
        menu.exec_(point)

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
            self.type_combo.setCurrentIndex(self.type_combo.count() + 1)
            self._set_filter_type("type")
        self._filter()

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

    def show_create_library_widget(self):
        """
        添加library
        :return:
        """
        create_library_widget = CreateLibraryWidget(self)
        create_library_widget.create.connect(self.add_library)
        create_library_widget.exec_()

    def add_library(self, args):
        """
        add library
        :param args:
        :return:
        """
        self.library_list_view.append_library(*args)