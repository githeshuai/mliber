# -*- coding:utf-8 -*-
from Qt.QtWidgets import *
from main_widget_ui import MainWidgetUI
from mliber_widgets.user_manage import UserManage
from mliber_widgets.library_manage import LibraryManage
import mliber_utils
import mliber_global
from mliber_api.database_api import Database
from mliber_qt_components.messagebox import MessageBox


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

    def auto_login(self):
        """
        自动登录
        :return:
        """
        app = mliber_global.app()
        need_remember = mliber_utils.read_history("need_remember")
        auto_login = mliber_utils.read_history("auto_login")
        if need_remember and auto_login:
            try:
                database = mliber_utils.read_history("database")
                user_name = mliber_utils.read_history("user")
                password = mliber_utils.read_history("password")
                db = Database(database)
                db.create_admin()
                app.set_value(mliber_database=db)
                user = db.find_one("User", [["name", "=", user_name]])
                if user and user.password == password and user.status == "Active":
                    app.set_value(mliber_user=user)
            except RuntimeError as e:
                MessageBox.critical(self, "Login Failed", str(e))
                return False
        return True

    def set_global_library_from_history(self):
        """
        根据历史记录获取library，并设置全局
        :return:
        """
        app = mliber_global.app()
        library_id = mliber_utils.read_history("library_id")
        if library_id:
            db = app.value("mliber_database")
            library = db.find_one("Library", [["id", "=", library_id]])
            if library:
                app.set_value(mliber_library=library)
                self.refresh_library()

    def showEvent(self, event):
        """
        在显示之前，获取历史记录，自动登录
        :return:
        """
        if self.auto_login():
            self.set_global_library_from_history()


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        mw = MainWidget()
        mw.show()
