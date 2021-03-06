# -*- coding:utf-8 -*-
from Qt.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLineEdit, QHBoxLayout, QToolButton, QCheckBox, \
    QPushButton, QSizePolicy, QDialog, QLabel
from Qt.QtCore import Qt, QSize
import mliber_resource
from mliber_qt_components.icon_line_edit import IconLineEdit
from mliber_qt_components.title_widget import TitleWidget


class LoginWidgetUI(QDialog):
    def __init__(self, parent=None):
        super(LoginWidgetUI, self).__init__(parent)
        self.setWindowTitle("Login")
        self.resize(350, 300)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        top_layout = QVBoxLayout(self)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(15)
        self.title = TitleWidget(self)
        # main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 10, 20, 10)
        self.database_combo = QComboBox(self)
        self.database_combo.setItemIcon(0, mliber_resource.icon("database.png"))
        self.database_combo.setMinimumHeight(30)
        self.user_le = IconLineEdit(mliber_resource.icon_path("user.png"), 30, 14, self)
        self.password_le = IconLineEdit(mliber_resource.icon_path("password.png"), 30, 14, self)
        self.password_le.setEchoMode(QLineEdit.Password)
        # layout
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.info_label = QToolButton(self)
        self.remember_me_check = QCheckBox("Remember Me", self)
        self.auto_login_check = QCheckBox("Auto Login", self)
        layout.addWidget(self.remember_me_check)
        layout.addWidget(self.auto_login_check)
        # login button
        self.login_btn = QPushButton("LOGIN")
        self.login_btn.setStyleSheet("QPushButton{height: 36px; font-family: Arial; font-size: 13px; font: bold; "
                                     "color: #fff;border: 0px; background: #4c9fcb;}"
                                     "QPushButton:hover{background: #59b8ea;}"
                                     "QPushButton:focus{outline: none;border: 0px;}")
        # info label
        info_layout = QHBoxLayout()
        self.info_label.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.info_label.setStyleSheet("border: 0px; padding: 0px; background: transparent;"
                                      "color: #F00; font: bold; font-size: 12px; height: 22px; font-family: Arial")
        self.info_label.setHidden(True)
        info_layout.addStretch()
        info_layout.addWidget(self.info_label)
        info_layout.addStretch()
        # add to main layout
        main_layout.addWidget(self.database_combo)
        main_layout.addWidget(self.user_le)
        main_layout.addWidget(self.password_le)
        main_layout.addLayout(layout)
        main_layout.addWidget(self.login_btn)
        main_layout.addLayout(info_layout)
        main_layout.setSpacing(20)
        # add to top
        top_layout.addWidget(self.title)
        top_layout.addLayout(main_layout)
