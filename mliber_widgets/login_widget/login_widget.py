# -*- coding:utf-8 -*-
from PySide.QtGui import *
from mliber_widgets.login_widget.login_widget_ui import LoginWidgetUI
import mliber_utils
import mliber_resource
from mliber_global.app_global import get_app_global
from mliber_qt_components.messagebox import MessageBox
from mliber_custom.database import DATABASES
from mliber_api.database_api import Database


class LoginWidget(LoginWidgetUI):
    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)
        # set signals
        self.set_signals()
        self.init_database()
        self.init_ui()

    def set_signals(self):
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
        print repr(need_remember)
        if need_remember:
            self.remember_me_check.setChecked(True)
        database = mliber_utils.read_history("database")
        self.database_combo.setCurrentIndex(self.database_combo.findText(database))
        self.user_le.setText(mliber_utils.read_history("user"))
        self.password_le.setText(mliber_utils.read_history("password"))

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

    def login_failed(self):
        """
        show error information
        Returns:
        """
        self.info_label.show()
        self.info_label.setIcon(mliber_resource.icon("error.png"))
        self.info_label.setText(u"Login Failed ！")

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
        except:
            MessageBox.critical(self, "Errir", u"不能连接数据库:%s" % self.database)
            return
        app_global = get_app_global()
        app_global.set_value(mliber_database=db)
        user = db.find_one("User", [["name", "=", self.user]])
        if user and user.password == self.password:
            app_global.set_value(mliber_user=user)
            self.write_history()
        else:
            self.login_failed()

    def write_history(self):
        """
        写出历史记录
        :return:
        """
        mliber_utils.write_history(need_remember=self.need_remember,
                                   database=self.database,
                                   user=self.user,
                                   password=self.password)
        self.deleteLater()


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        tw = LoginWidget()
        tw.show()
