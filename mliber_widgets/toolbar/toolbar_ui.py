# -*- coding:utf-8 -*-
from Qt.QtWidgets import *
from Qt.QtCore import *
import mliber_resource


class ToolbarUI(QWidget):
    def __init__(self, parent=None):
        super(ToolbarUI, self).__init__(parent)
        self.setFixedHeight(50)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # logo button
        logo_button = QToolButton(self)
        # logo_button.setMinimumHeight(40)
        logo_button.setIconSize(QSize(40, 40))
        logo_button.setStyleSheet("font: 20px; border: 0x; background: transparent; padding: 0px;")
        logo_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        logo_button.setIcon(mliber_resource.icon("logo.png"))
        logo_button.setText("mliber")
        # login
        self.login_button = QPushButton("Login", self)
        # settings
        self.settings_button = QPushButton("Settings", self)
        # button layout
        button_layout = QHBoxLayout()
        self.minimum_btn = QToolButton(self)
        self.minimum_btn.setIcon(mliber_resource.icon("minus.png"))
        self.minimum_btn.setStyleSheet("QToolButton{background-color: rgb(255, 255, 255, 10); "
                                       "padding:0px; border: 0px solid;}"
                                       "QToolButton::hover{background-color: #707070}")
        self.maximum_btn = QToolButton(self)
        self.maximum_btn.setIcon(mliber_resource.icon("max.png"))
        self.maximum_btn.setStyleSheet("QToolButton{background-color: rgb(255, 255, 255, 10);"
                                       "padding:0px; border: 0px solid;} "
                                       "QToolButton::hover{background-color: #707070}")
        self.close_btn = QToolButton(self)
        self.close_btn.setIcon(mliber_resource.icon("close.png"))
        self.close_btn.setStyleSheet("QToolButton{background-color: rgb(255, 255, 255, 10); "
                                     "padding:0px; border: 0px solid;}"
                                     "QToolButton::hover{background-color: #D50000}")
        button_layout.addWidget(self.minimum_btn)
        button_layout.addWidget(self.maximum_btn)
        button_layout.addWidget(self.close_btn)
        # add to main layout
        main_layout.addWidget(logo_button)
        main_layout.addWidget(self.login_button)
        main_layout.addWidget(self.settings_button)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        tw = ToolbarUI()
        tw.show()

