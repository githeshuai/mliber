# -*- coding:utf-8 -*-
from Qt.QtWidgets import QWidget, QHBoxLayout, QToolButton, QPushButton, QFrame, QSpacerItem, QSizePolicy
from Qt.QtCore import QSize, Qt
import mliber_resource
import mliber_version
from mliber_qt_components.indicator_button import IndicatorButton
from mliber_qt_components.toolbutton import ToolButton


class ToolbarUI(QFrame):
    def __init__(self, parent=None):
        super(ToolbarUI, self).__init__(parent)
        self.setFixedHeight(45)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # logo button
        logo_button = QToolButton(self)
        # logo_button.setMinimumHeight(40)
        logo_button.setIconSize(QSize(27, 27))
        logo_button.setStyleSheet("font: bold; font-size: 13px; border: 0x; background: transparent; "
                                  "padding: 0px; color: #fff;")
        logo_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        logo_button.setIcon(mliber_resource.icon("logo.png"))
        logo_button.setText("M-Liber %s" % mliber_version.VERSION)
        # spacer item
        space_item_1 = QSpacerItem(20, 40, QSizePolicy.Fixed, QSizePolicy.Expanding)
        # login
        self.login_button = IndicatorButton("Login", self)
        # settings
        self.settings_button = IndicatorButton("Settings", self)
        # window
        self.window_button = IndicatorButton("Window", self)
        # library
        self.library_button = IndicatorButton("", self)
        self.library_button.setMinimumWidth(200)
        # user
        self.user_button = ToolButton(self)
        self.user_button.set_icon("user_fill.png")
        self.user_button.setText("User")
        space_item_2 = QSpacerItem(50, 40, QSizePolicy.Fixed, QSizePolicy.Expanding)
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
        main_layout.addItem(space_item_1)
        main_layout.addWidget(self.login_button)
        main_layout.addWidget(self.settings_button)
        main_layout.addWidget(self.window_button)
        main_layout.addStretch()
        main_layout.addWidget(self.library_button)
        main_layout.addStretch()
        main_layout.addWidget(self.user_button)
        main_layout.addItem(space_item_2)
        main_layout.addLayout(button_layout)


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        tw = ToolbarUI()
        tw.show()

