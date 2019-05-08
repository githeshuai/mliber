# -*- coding:utf-8 -*-
from datetime import datetime
from Qt.QtWidgets import QMenu, QAction, QInputDialog, QLineEdit
from Qt.QtGui import QCursor
from Qt.QtCore import Signal, Qt
from library_manage_ui import LibraryManageUI
from create_library_dialog import CreateLibraryDialog
import mliber_resource
import mliber_global
from mliber_conf.library_type import LIBRARY_TYPE
from mliber_api.database_api import Database
from mliber_qt_components.messagebox import MessageBox


class LibraryManage(LibraryManageUI):
    library_double_clicked = Signal()

    def __init__(self, parent=None):
        super(LibraryManage, self).__init__(parent)
        # set style
        self.set_style()
        # set signals
        self._set_signals()
        # init
        self.init()
        # 右键菜单
        self.library_list_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.library_list_view.customContextMenuRequested.connect(self.show_context_menu)

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
        self.refresh_btn.clicked.connect(self.refresh_ui)
        self.library_list_view.double_clicked.connect(self.on_library_list_view_double_clicked)

    @property
    def user(self):
        return mliber_global.app().value("mliber_user")

    def on_library_list_view_double_clicked(self):
        """
        当library list view 双击的时候
        :return:
        """
        self.library_double_clicked.emit()
        self.close()

    def add_menu(self):
        """
        menu bar add menu
        :return:
        """
        menu = QMenu(self)
        if self.user.library_permission:
            add_action = QAction("Add", self, triggered=self.show_create_library_dialog)
            menu.addAction(add_action)
        exit_action = QAction("exit", self, triggered=self.close)
        menu.addAction(exit_action)
        point = self.menu_bar.rect().bottomLeft()
        point = self.menu_bar.mapToGlobal(point)
        menu.exec_(point)

    def show_context_menu(self):
        """
        显示右键菜单
        :return:
        """
        selected_library = self.library_list_view.selected_item()
        menu = QMenu(self)
        if selected_library:
            action_text = "Edit" if self.user.library_permission else "Detail"
            edit_action = QAction(action_text, menu, triggered=self.show_edit_library_dialog)
            menu.addAction(edit_action)
            if self.user.library_permission:
                delete_action = QAction("Delete", menu, triggered=self.delete_library)
                menu.addAction(delete_action)
        else:
            refresh_action = QAction("Refresh", menu, triggered=self.refresh_ui)
            menu.addAction(refresh_action)
        menu.exec_(QCursor.pos())

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

    def show_create_library_dialog(self):
        """
        添加library
        :return:
        """
        self.library_widget = CreateLibraryDialog(mode="create", parent=self)
        self.library_widget.create.connect(self.add_library)
        self.library_widget.exec_()

    def show_edit_library_dialog(self):
        """
        edit current selected library
        :return:
        """
        selected_item = self.library_list_view.selected_item()
        self.library_widget = CreateLibraryDialog(mode="update", parent=self)
        self.library_widget.update.connect(self.update_library)
        if not self.user.library_permission:
            self.library_widget.exec_button.setHidden(True)
        self.library_widget.set_name(selected_item.library.name)
        self.library_widget.set_type(selected_item.library.type)
        self.library_widget.set_windows_path(selected_item.library.windows_path)
        self.library_widget.set_linux_path(selected_item.library.linux_path)
        self.library_widget.set_mac_path(selected_item.library.mac_path)
        self.library_widget.set_icon_path(selected_item.icon_path)
        self.library_widget.set_description(selected_item.library.description)
        self.library_widget.exec_()

    def add_library(self, args):
        """
        add library
        :param args:
        :return:
        """
        add_result = self.library_list_view.append_library(*args)
        if add_result:
            self.library_widget.accept()
            
    def update_library(self, args):
        """
        update current selected library
        :return:
        """
        update_result = self.library_list_view.update_library(*args)
        if update_result:
            self.refresh_ui()
            self.library_widget.accept()

    def refresh_ui(self):
        """
        刷新ui
        :return:
        """
        self.library_list_view.refresh_ui()
        self._filter()

    def delete_library(self):
        """
        delete current library
        :return:
        """
        # 输入密码验证
        password, ok = QInputDialog.getText(self, "Password", "Input Password", echo=QLineEdit.Password)
        if password and ok:
            if password != self.user.password:
                MessageBox.critical(self, "Wrong Password", u"密码错误")
                return
        selected_library = self.library_list_view.selected_library()
        db = Database(mliber_global.app().value("mliber_database"))
        db.update("Library", selected_library.id, {"status": "Disable",
                                                   "updated_at": datetime.now(),
                                                   "updated_by": self.user.id})
        if mliber_global.app().value("mliber_library") == selected_library:
            mliber_global.app().set_value(mliber_library=None)
        self.refresh_ui()
