# -*- coding:utf-8 -*-
from Qt.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QCheckBox, QToolButton, QPushButton
from Qt.QtCore import Qt, Signal, QSize
import mliber_resource
import mliber_global


class DeleteWidget(QDialog):
    accept_signal = Signal(bool)

    def __init__(self, parent=None):
        super(DeleteWidget, self).__init__(parent)
        self.resize(350, 140)
        top_layout = QVBoxLayout(self)
        top_layout.setSpacing(20)
        top_layout.setContentsMargins(0, 0, 0, 0)
        title_widget = QPushButton(self)
        title_widget.setMinimumHeight(50)
        title_widget.setStyleSheet("background: #2d2f37; padding: 0px; font: bold; "
                                   "font-size: 15px; border: none; color: #F00;")
        title_widget.setText("    Do you really want to delete it ?")
        title_widget.setIcon(mliber_resource.icon("warning_red.png"))
        title_widget.setIconSize(QSize(40, 40))
        top_layout.addWidget(title_widget)
        # main
        main_layout = QVBoxLayout()
        top_layout.addLayout(main_layout)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(10)
        self.setWindowTitle("Delete Category")
        # password layout
        password_layout = QVBoxLayout()
        text_label = QLabel(self)
        text_label.setFixedHeight(20)
        text_label.setText(u"Please input password")
        self.password_le = QLineEdit(self)
        self.password_le.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(text_label)
        password_layout.addWidget(self.password_le)
        password_layout.setSpacing(2)
        # layout include checkbox and info label
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft)
        self.check = QCheckBox("Delete storage files", self)
        self.info_label = QToolButton(self)
        self.info_label.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.info_label.setStyleSheet("border: 0px; padding: 0px; background: transparent;"
                                      "color: #F00; font: bold; font-size: 12px; height: 22px; font-family: Arial")
        self.info_label.setHidden(True)
        layout.addWidget(self.check)
        layout.addStretch()
        layout.addWidget(self.info_label)
        layout.addStretch()
        # button layout
        button_layout = QHBoxLayout()
        self.ok_btn = QPushButton("Ok", self)
        self.close_btn = QPushButton("Cancel", self)
        button_layout.addStretch()
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.close_btn)
        # add to main layout
        main_layout.addLayout(password_layout)
        main_layout.addLayout(layout)
        main_layout.addLayout(button_layout)
        # set signals
        self._set_signals()

    def _set_signals(self):
        """
        信号连接
        :return:
        """
        self.ok_btn.clicked.connect(self.on_ok_button_clicked)
        self.close_btn.clicked.connect(self._close)

    @property
    def password(self):
        """
        密码
        :return:
        """
        return self.password_le.text()

    @property
    def delete_source(self):
        """
        是否删除源文件
        :return: <bool>
        """
        return self.check.isChecked()

    def _login_failed(self):
        """
        show error information
        Returns:
        """
        self.info_label.setHidden(False)
        self.info_label.setIcon(mliber_resource.icon("error.png"))
        self.info_label.setText("Wrong Password !")

    def validate_password(self):
        """
        检查密码是否正确
        :return:
        """
        user = mliber_global.user()
        password = user.password
        if self.password == password:
            return True
        return False

    def on_ok_button_clicked(self):
        """
        当ok按钮按下的时候
        :return:
        """
        if self.validate_password():
            self.accept_signal.emit(self.delete_source)
            self._close()
        else:
            self._login_failed()

    def _close(self):
        """

        :return:
        """
        self.close()
        self.deleteLater()


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        d = DeleteWidget()
        d.show()
