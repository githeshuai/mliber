# -*- coding:utf-8 -*-
from Qt.QtWidgets import QDialog, QVBoxLayout, QGridLayout, QLineEdit, QHBoxLayout, QPushButton, QLabel
from Qt.QtCore import Qt
import mliber_global
import mliber_resource
from mliber_qt_components.messagebox import MessageBox
from mliber_qt_components.icon_line_edit import IconLineEdit
from mliber_qt_components.title_widget import TitleWidget


class PasswordWidget(QDialog):
    def __init__(self, parent=None):
        super(PasswordWidget, self).__init__(parent)
        self.resize(320, 200)
        self.setWindowTitle("Change password")
        self.setFocusPolicy(Qt.NoFocus)
        top_layout = QVBoxLayout(self)
        top_layout.setContentsMargins(0, 0, 0, 0)
        title_widget = TitleWidget()
        top_layout.addWidget(title_widget)
        # main
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        top_layout.addLayout(main_layout)
        main_layout.setContentsMargins(5, 5, 5, 10)
        # old password
        password_layout = QGridLayout()
        old_password_label = QLabel(u"旧密码", self)
        old_password_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.old_password_le = IconLineEdit(mliber_resource.icon_path("password.png"), 30, 14, self)
        self.old_password_le.setEchoMode(QLineEdit.Password)
        # new password
        new_password_label = QLabel(u"新密码", self)
        new_password_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.new_password_le = IconLineEdit(mliber_resource.icon_path("password.png"), 30, 14, self)
        self.new_password_le.setEchoMode(QLineEdit.Password)
        # repeat password
        repeat_password_label = QLabel(u"新密码", self)
        repeat_password_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.repeat_password_le = IconLineEdit(mliber_resource.icon_path("password.png"), 30, 14, self)
        self.repeat_password_le.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(old_password_label, 0, 0, 1, 1)
        password_layout.addWidget(self.old_password_le, 0, 1, 1, 6)
        password_layout.addWidget(new_password_label, 1, 0, 1, 1)
        password_layout.addWidget(self.new_password_le, 1, 1, 1, 6)
        password_layout.addWidget(repeat_password_label, 2, 0, 1, 1)
        password_layout.addWidget(self.repeat_password_le, 2, 1, 1, 6)
        password_layout.setVerticalSpacing(15)
        # button layout
        button_layout = QHBoxLayout()
        self.ok_btn = QPushButton("Ok", self)
        self.cancel_btn = QPushButton("Cancel", self)
        button_layout.addStretch()
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)
        # add to main layout
        main_layout.addLayout(password_layout)
        main_layout.addLayout(button_layout)
        # set signals
        self.set_signals()

    def set_signals(self):
        self.cancel_btn.clicked.connect(self.close)
        self.ok_btn.clicked.connect(self.change_password)

    @property
    def old_password(self):
        """
        :return:
        """
        return self.old_password_le.text()

    @property
    def new_password(self):
        """
        :return:
        """
        return self.new_password_le.text()

    @property
    def repeat_new_password(self):
        """
        :return:
        """
        return self.repeat_password_le.text()

    def change_password(self):
        """
        改变密码
        :return:
        """
        user = mliber_global.user()
        if user:
            old_password = user.password
            if old_password != self.old_password:
                MessageBox.critical(self, "Error", u"旧密码错误")
                return
            if self.new_password != self.repeat_new_password:
                MessageBox.critical(self, "Error", u"两次输入的新密码不一样")
                return
            with mliber_global.db() as db:
                db.update("User", user.id, {"password": self.new_password})
        self.close()


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        pw = PasswordWidget()
        pw.show()
