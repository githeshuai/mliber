# -*- coding:utf-8 -*-
"""
用来做进度显示
"""

from Qt.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTextEdit, QProgressBar, QPushButton, QApplication


class InfoWidget(QWidget):
    def __init__(self, parent=None):
        super(InfoWidget, self).__init__(parent)
        self.has_started = False
        self.resize(400, 350)
        self.setWindowTitle("Information")
        # setup ui
        main_layout = QVBoxLayout(self)
        self.info_te = QTextEdit(self)

        progress_layout = QHBoxLayout()
        progress_layout.setContentsMargins(0, 0, 0, 0)
        self.progress_bar = QProgressBar(self)
        self.cancel_btn = QPushButton("Ok", self)
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.cancel_btn)

        self.cancel_btn.setMaximumHeight(25)

        main_layout.addWidget(self.info_te)
        main_layout.addLayout(progress_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # set signals
        self.set_signals()

    def set_button_shown(self, show_status):
        """
        :param show_status: <bool>
        :return:
        """
        self.cancel_btn.setHidden(not show_status)

    def set_signals(self):
        """
        信号连接
        :return:
        """
        self.cancel_btn.clicked.connect(self.close)

    def append(self, text):
        """
        :param text: <str>
        :return:
        """
        self.info_te.append(text)
        app = QApplication.instance()
        app.processEvents()

    def append_info(self, text):
        """
        增加显示信息， 显示为白色
        :param text:
        :return:
        """
        self.append("<font family=Arial color=#FFF>[MLIBER] info: %s</font>" % text)

    def append_warning(self, text):
        """
        增加warning信息， 显示为黄色信息
        :param text:
        :return:
        """
        self.append("<font family=Arial color=#FFD700>[MLIBER] warning: %s</font>" % text)

    def append_error(self, text):
        """
        增加错误信息， 显示为红色
        :param text:
        :return:
        """
        self.append("<font family=Arial color=#F00>[MLIBER] error: %s</font>" % text)

    def append_pass(self, text):
        """
        增加通过信息， 显示为绿色
        :param text:
        :return:
        """
        self.append("<font family=Arial color=#32CD32>[MLIBER] pass: %s</font>" % text)

    def set_progress_range(self, start, end):
        """
        设置进度条的区间
        :param start: <int>
        :param end: <int>
        :return:
        """
        self.progress_bar.setRange(start, end)

    def set_progress_value(self, value):
        """
        设置进度条的值
        :param value: <int>
        :return:
        """
        self.progress_bar.setValue(value)
        app = QApplication.instance()
        app.processEvents()

    def start(self):
        """
        开始显示
        :return:
        """
        self.has_started = True
        self.info_te.clear()
        self.cancel_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.show()
        app = QApplication.instance()
        app.processEvents()

    def finish(self):
        """
        :return:
        """
        self.cancel_btn.setEnabled(True)
