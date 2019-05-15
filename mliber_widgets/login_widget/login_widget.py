# -*- coding:utf-8 -*-
import logging
from Qt.QtWidgets import QDesktopWidget
from Qt.QtCore import Signal
from mliber_widgets.login_widget.login_widget_ui import LoginWidgetUI
import mliber_utils
import mliber_resource
import mliber_global
from mliber_custom.database import DATABASES
from mliber_api.database_api import Database


class LoginWidget(LoginWidgetUI):
    login_succeed = Signal()

    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)
        # set signals
        self._set_signals()
        self.init_database()
        self.init_ui()

    def _set_signals(self):
        """
        信号连接
        :return:
        """
        self.login_btn.clicked.connect(self.login)

    def init_ui(self):
        """
        初始化ui
        :return:
        """
        need_remember = mliber_utils.read_history("need_remember")
        auto_login = mliber_utils.read_history("auto_login")
        if need_remember:
            self.remember_me_check.setChecked(True)
            database = mliber_utils.read_history("database")
            self.database_combo.setCurrentIndex(self.database_combo.findText(database))
            self.user_le.setText(mliber_utils.read_history("user"))
            self.password_le.setText(mliber_utils.read_history("password"))
        if auto_login:
            self.auto_login_check.setChecked(True)

    def init_database(self):
        """
        :return:
        """
        databases = DATABASES.keys()
        self.database_combo.addItems(databases)

    def move_to_center(self):
        """
        move to desktop center
        Returns:
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def _report_error(self, error_info):
        """
        显示错误信息
        :return:
        """
        self.info_label.setText(error_info)
        self.info_label.setIcon(mliber_resource.icon("error.png"))
        self.info_label.show()
        self.resize(320, 330)

    def login_failed(self):
        """
        show error information
        Returns:
        """
        self._report_error("Login Failed !")

    def connect_failed(self):
        """
        连接数据库失败
        :return:
        """
        self._report_error("Connect Database Failed !")

    @property
    def database(self):
        """
        选择的数据库名
        :return:
        """
        return self.database_combo.currentText()

    @property
    def user(self):
        """
        用户名
        :return:
        """
        return self.user_le.text()

    @property
    def password(self):
        """
        密码
        :return:
        """
        return self.password_le.text()

    @property
    def need_remember(self):
        """
        记录历史
        :return: <int>
        """
        return 1 if self.remember_me_check.isChecked() else 0

    @property
    def auto_login(self):
        """
        自动登录
        :return:
        """
        return 1 if self.auto_login_check.isChecked() else 0

    def validate(self):
        """
        检查是否填了user password
        :return:
        """
        if not all((self.database, self.user, self.password)):
            return False
        return True

    def login(self):
        """
        登录
        :return:
        """
        if not self.validate():
            return
        try:
            db = Database(self.database)
            db.create_admin()
        except Exception as e:
            logging.critical(str(e))
            self.connect_failed()
            return
        self.login_succeed.emit()
        app = mliber_global.app()
        app.set_value(mliber_database=self.database)
        user = db.find_one("User", [["name", "=", self.user]])
        if user and user.password == self.password and user.status == "Active":
            app.set_value(mliber_user=user)
            self.write_history()
        else:
            self.login_failed()

    def write_history(self):
        """
        写出历史记录
        :return:
        """
        mliber_utils.write_history(need_remember=self.need_remember,
                                   auto_login=self.auto_login,
                                   database=self.database,
                                   user=self.user,
                                   password=self.password)
        self.deleteLater()


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        tw = LoginWidget()
        tw.show()
