# -*- coding:utf-8 -*-
from Qt.QtWidgets import QWidget, QToolButton, QVBoxLayout, QHBoxLayout, QButtonGroup, QStackedLayout, QAbstractButton
from Qt.QtCore import Qt, QSize
from mliber_qt_components.drag_file_widget import DragFileWidget
from mliber_qt_components.screen_shot import ScreenShotWidget
import mliber_resource
from mliber_libs.python_libs.sequence_converter import Converter


BUTTONS = [{"name": u"截图", "icon": "screen.png", "type": "screen"},
           {"name": u"图片", "icon": "picture.png", "type": "image"},
           {"name": u"序列", "icon": "sequence.png", "type": "sequence"},
           {"name": u"视频", "icon": "video.png", "type": "video"}]


class ThumbnailWidget(QWidget):
    def __init__(self, parent=None):
        super(ThumbnailWidget, self).__init__(parent)
        self._current_index = 0
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # top button layout
        self.button_layout = QHBoxLayout()
        self.btn_grp = QButtonGroup(self)
        # stacked layout
        self.stacked_layout = QStackedLayout()
        self.stacked_layout.setAlignment(Qt.AlignCenter)
        # screen shot widget
        widget = QWidget(self)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.screen_shot_widget = ScreenShotWidget(self)
        self.screen_shot_widget.setFixedSize(200, 200)
        layout.addWidget(self.screen_shot_widget)
        layout.setAlignment(Qt.AlignCenter)
        # drag file widget
        self.file_widget = DragFileWidget(self)
        # add to stacked layout
        self.stacked_layout.addWidget(widget)
        self.stacked_layout.addWidget(self.file_widget)
        # add to main layout
        main_layout.addLayout(self.button_layout)
        main_layout.addLayout(self.stacked_layout)
        # init
        self.init_buttons()
        # set signals
        self._set_signals()

    def init_buttons(self):
        """
        添加button
        :return:
        """
        for index, item in enumerate(BUTTONS):
            text = item.get("name")
            icon = item.get("icon")
            button = QToolButton(self)
            button.setMaximumHeight(20)
            button.setText(text)
            button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            icon_size = button.height() * 0.8
            button.setIconSize(QSize(icon_size, icon_size))
            button.setIcon(mliber_resource.icon(icon))
            button.index = index
            self.button_layout.addWidget(button)
            self.btn_grp.addButton(button)

    def _set_signals(self):
        """
        信号连接
        :return:
        """
        self.btn_grp.buttonClicked[QAbstractButton].connect(self._switch)

    def _switch(self, button):
        """
        switch stacked layout
        :param button:
        :return:
        """
        self._current_index = button.index
        if button.index == 0:
            self.stacked_layout.setCurrentIndex(0)
        else:
            self.stacked_layout.setCurrentIndex(1)
            self.file_widget.clear()

    def current_type(self):
        """
        获取当前type
        :return:
        """
        item = BUTTONS[self._current_index]
        return item.get("type")

    def files(self):
        """
        获取当前thumbnail files
        :return:
        """
        current_type = self.current_type()
        if current_type == "screen":
            return [self.screen_shot_widget.get_thumbnail_path()]
        else:
            return self.file_widget.item_texts()

    def convert_to(self, dst_pattern):
        """
        转换缩略图
        :param dst_pattern: /xxx/xxx/xxx.####.png
        :return:
        """
        files = self.files()
        if not files:
            return
        converter = Converter(self.current_type())
        converter.convert(files, dst_pattern)


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        tw = ThumbnailWidget()
        tw.show()
