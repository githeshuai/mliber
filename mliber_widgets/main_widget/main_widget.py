# -*- coding:utf-8 -*-
from Qt.QtWidgets import *
from main_widget_ui import MainWidgetUI
from mliber_widgets.user_manage import UserManage
from mliber_widgets.library_manage import LibraryManage


class MainWidget(MainWidgetUI):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        # set signals
        self.set_signals()

    def set_signals(self):
        """
        信号连接
        :return:
        """
        self.tool_bar.user_manage_action_triggered.connect(self.show_user_manager)
        self.tool_bar.library_manage_action_triggered.connect(self.show_library_manager)

    def show_user_manager(self):
        """
        显示user manager
        :return:
        """
        user_manage_ui = UserManage(self)
        user_manage_ui.exec_()

    def show_library_manager(self):
        """
        显示library manager
        :return:
        """
        library_manage_ui = LibraryManage(self)
        library_manage_ui.library_double_clicked.connect(self.refresh_library)
        library_manage_ui.exec_()

    def refresh_library(self):
        """
        刷新library
        :return:
        """
        self.category_widget.category_tree.refresh_global()
        self.category_widget.category_tree.refresh_data()


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        mw = MainWidget()
        mw.show()
