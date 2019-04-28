# -*- coding: utf-8 -*-
import time
from Qt.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QPushButton, QLineEdit, \
    QDesktopWidget, QHBoxLayout, QToolButton, QLabel, QDialog
from Qt.QtCore import QSize, Qt, Signal

import mliber_resource
import mliber_utils
from mliber_qt_components.frameless_widget import FramelessWidget
from mliber_qt_components.icon_line_edit import IconLineEdit


LE_HEIGHT = 30
FONT_SIZE = 15


class LoginCentralWidget(QWidget):
    def __init__(self, parent=None):
        super(LoginCentralWidget, self).__init__(parent)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.user_icon_label = QLabel(self)
        self.user_icon_label.setStyleSheet("background: transparent;")
        self.user_icon_label.setAlignment(Qt.AlignCenter)
        # user
        self.user_le = IconLineEdit(mliber_resource.icon_path("user.png"), LE_HEIGHT, FONT_SIZE, self)
        self.user_le.setPlaceholderText("Username")
        # checkbox
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.remember_me_check = QCheckBox("Remember me")
        self.remember_me_check.setFocusPolicy(Qt.NoFocus)
        self.remember_me_check.setStyleSheet("color: #fff")
        self.info_label = QToolButton()
        self.info_label.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.info_label.setStyleSheet("border: 0px; padding: 0px; background: transparent;"
                                      "color: #F00; font: bold; font-size: 12px; height: 22px; font-family: Arial")
        layout.addWidget(self.remember_me_check)
        layout.addWidget(self.info_label)
        # login button
        self.login_btn = QPushButton("LOGIN")
        self.login_btn.setStyleSheet("QPushButton{height: 36px; font-family: Arial; font-size: 13px; font: bold; "
                                     "color: #fff;border: 0px; background: #4c9fcb;}"
                                     "QPushButton:hover{background: #59b8ea;}"
                                     "QPushButton:focus{background: #008B8B;}")
        main_layout.addStretch()
        main_layout.addWidget(self.user_icon_label)
        main_layout.addStretch()
        main_layout.addWidget(self.user_le)
        main_layout.addLayout(layout)
        main_layout.addWidget(self.login_btn)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 0, 20, 0)
        # set logo
        self.set_logo()
        # set style
        self.setStyleSheet(mliber_resource.style())

    def set_logo(self):
        pixmap = mliber_resource.pixmap("login_user.png")
        pixmap = pixmap.scaled(QSize(120, 120), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.user_icon_label.setPixmap(pixmap)


class LoginWidget(FramelessWidget):

    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)
        self.sg_opt = None
        self.user = None
        self.setFixedSize(320, 404)
        self.set_window_flag("dialog")
        central_widget = LoginCentralWidget(self)
        self.set_central_widget(central_widget)
        self.set_background_color(mliber_resource.icon_path("login_background.png"))
        self.user_le = central_widget.user_le
        self.remember_me_check = central_widget.remember_me_check
        self.info_label = central_widget.info_label
        self.login_btn = central_widget.login_btn
        self.move_to_center()
        self.set_signals()

    def set_signals(self):
        self.login_btn.clicked.connect(self.login)

    def move_to_center(self):
        """
        move to desktop center
        Returns:
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def get_user(self):
        return self.user_le.text()

    @property
    def need_remember(self):
        """
        Returns: <bool>
        """
        return 1 if self.remember_me_check.isChecked() else ""

    def log_failed(self):
        """
        show error information
        Returns:
        """
        self.info_label.setIcon(mliber_resource.icon("error.png"))
        self.info_label.setText("Login Failed. please try again")

    def login_successful(self):
        """
        write out history
        Returns:
        """
        mliber_utils.write_history(need_remember=self.need_remember, user=self.user)
        self.deleteLater()

    def login(self):
        """
        login
        Returns:
        """
        self.user = self.get_user()
        try:
            start = time.time()
            sg_opt = SgOpt()
            self.sg_opt = sg_opt
            print u"登陆用时:%s" % (time.time() - start)
            user_info = sg_opt.find_user(self.user)
            if user_info:
                self.login_successful()
            else:
                self.log_failed()
        except Exception as e:
            print "[LIBER] error: {}".format(str(e))
            self.log_failed()

    def showEvent(self, event):
        need_remember = mliber_utils.read_history("need_remember")
        if need_remember:
            user = mliber_utils.read_history("user")
            if user:
                self.remember_me_check.setChecked(True)
                self.user_le.setText(user)


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        lw = LoginWidget()
        lw.show()


        

