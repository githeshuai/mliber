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
from mliber_qt_components.messagebox import MessageBox
from mliber_qt_components.delete_widget import DeleteWidget
from mliber_libs.os_libs.path import Path


class LibraryManage(LibraryManageUI):
    library_double_clicked = Signal()
    deleted = Signal()

    def __init__(self, parent=None):
        super(LibraryManage, self).__init__(parent)
        # set signals
        self._set_signals()
        # 右键菜单
        self.library_list_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.library_list_view.customContextMenuRequested.connect(self._show_context_menu)

    def refresh_ui(self):
        """
        initialize
        :return:
        """
        # show data
        self.library_list_view.show_data()
        library_names = self.library_list_view.library_names()
        self.search_le.set_completer(library_names)
        self.type_combo.addItems(LIBRARY_TYPE)
        # filter
        self._filter()

    def _set_signals(self):
        """
        信号链接
        :return:
        """
        self.search_btngrp.buttonClicked.connect(self._switch_search_type)
        self.search_le.return_pressed.connect(self._filter)
        self.type_combo.currentIndexChanged.connect(self._filter)
        self.menu_bar.clicked.connect(self.add_menu)
        self.refresh_btn.clicked.connect(self.refresh_ui)
        self.library_list_view.double_clicked.connect(self.on_library_list_view_double_clicked)

    @property
    def user(self):
        return mliber_global.user()

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
            add_action = QAction("Add", self, triggered=self._show_create_library_dialog)
            menu.addAction(add_action)
        exit_action = QAction("exit", self, triggered=self.close)
        menu.addAction(exit_action)
        point = self.menu_bar.rect().bottomLeft()
        point = self.menu_bar.mapToGlobal(point)
        menu.exec_(point)

    def _show_context_menu(self):
        """
        显示右键菜单
        :return:
        """
        selected_item = self.library_list_view.selected_item()
        menu = QMenu(self)
        if selected_item:
            action_text = "Edit" if self.user.library_permission else "Detail"
            edit_action = QAction(action_text, menu, triggered=self._show_edit_library_dialog)
            menu.addAction(edit_action)
            menu.addSeparator()
            if self.user.library_permission:
                delete_action = QAction(mliber_resource.icon("delete.png"), "Send to Trash", menu,
                                        triggered=self._show_delete_widget)
                menu.addAction(delete_action)
        else:
            refresh_action = QAction("Refresh", menu, triggered=self.refresh_ui)
            menu.addAction(refresh_action)
        menu.exec_(QCursor.pos())

    def _switch_search_type(self, button):
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

    def _show_create_library_dialog(self):
        """
        添加library
        :return:
        """
        self.library_widget = CreateLibraryDialog(mode="create", parent=self)
        self.library_widget.create.connect(self._add_library)
        self.library_widget.exec_()

    def _show_edit_library_dialog(self):
        """
        edit current selected library
        :return:
        """
        selected_item = self.library_list_view.selected_item()
        self.library_widget = CreateLibraryDialog(mode="update", parent=self)
        self.library_widget.update.connect(self.update_library)
        if not self.user.library_permission:
            self.library_widget.exec_button.setHidden(True)
        self.library_widget.set_name(selected_item.name)
        self.library_widget.set_type(selected_item.type)
        self.library_widget.set_windows_path(selected_item.windows_path)
        self.library_widget.set_linux_path(selected_item.linux_path)
        self.library_widget.set_mac_path(selected_item.mac_path)
        self.library_widget.set_icon_path(selected_item.icon_path)
        self.library_widget.set_description(selected_item.description)
        self.library_widget.exec_()

    def _add_library(self, args):
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

    def _show_delete_widget(self):
        """
        显示删除窗口
        :return:
        """
        delete_widget = DeleteWidget(self)
        delete_widget.accept_signal.connect(self._delete_library)
        delete_widget.exec_()

    def _delete_library(self, delete_source):
        """
        delete current library
        :return:
        """
        # 输入密码验证
        source_model = self.library_list_view.model().sourceModel()
        selected_rows = self.library_list_view.selected_rows()
        row = selected_rows[0]
        selected_library = source_model.model_data[row].library
        with mliber_global.db() as db:
            self._delete(db, selected_library.id)
        if mliber_global.library() == selected_library:
            mliber_global.app().set_value(mliber_library=None)
            self.deleted.emit()
        # remove from list view
        source_model.removeRows(row, 1)
        # delete source
        if delete_source:
            try:
                Path(selected_library.root_path()).remove()
            except WindowsError as e:
                print str(e)
                MessageBox.warning(self, "Warning", u"源文件删除失败，请手动删除")

    def _delete(self, db, library_id):
        """
        删除library下的category和asset
        :param db:
        :param library_id:
        :return:
        """
        db.update("Library", library_id, {"status": "Disable",
                                          "updated_at": datetime.now(),
                                          "updated_by": self.user.id})
        categories = db.find("Category", [["library_id", "=", library_id], ["status", "=", "Active"]])
        for category in categories:
            db.update("Category", category.id, {"status": "Disable",
                                                "updated_at": datetime.now(),
                                                "updated_by": self.user.id})
        assets = db.find("Asset", [["library_id", "=", library_id], ["status", "=", "Active"]])
        for asset in assets:
            db.update("Asset", asset.id, {"status": "Disable",
                                          "updated_at": datetime.now(),
                                          "updated_by": self.user.id})
