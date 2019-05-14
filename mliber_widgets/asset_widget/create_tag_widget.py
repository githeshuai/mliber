# -*- coding:utf-8 -*-
from Qt.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QToolButton, QScrollArea, QWidget, QLineEdit, QPushButton
from Qt.QtCore import Qt, Signal
from Qt.QtGui import QColor
import mliber_resource
import mliber_global
from mliber_qt_components.search_line_edit import SearchLineEdit
from mliber_qt_components.icon_button import IconButton
from mliber_qt_components.toolbutton import ToolButton


class CreateTagWidget(QDialog):
    ok_clicked = Signal(list)

    def __init__(self, parent=None):
        super(CreateTagWidget, self).__init__(parent)
        self.setFixedWidth(400)
        self.setMinimumHeight(350)
        # setup ui
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        # top btn layout
        top_btn_layout = QHBoxLayout()
        top_btn_layout.setContentsMargins(0, 0, 0, 0)
        # add tag btn
        self.add_tag_btn = ToolButton(self)
        self.add_tag_btn.setMinimumHeight(30)
        self.add_tag_btn.setIcon(mliber_resource.icon("add.png"))
        self.add_tag_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.add_tag_btn.setText("New Tag")
        self.add_tag_btn.setStyleSheet("QToolButton{background: transparent; border: 0px solid;}")
        # search tag btn
        self.search_tag_btn = ToolButton(self)
        self.search_tag_btn.setMinimumHeight(30)
        self.search_tag_btn.setIcon(mliber_resource.icon("search.png"))
        self.search_tag_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.search_tag_btn.setStyleSheet("QToolButton{background: transparent; border: 0px solid;}")
        top_btn_layout.addWidget(self.add_tag_btn)
        top_btn_layout.addStretch()
        top_btn_layout.addWidget(self.search_tag_btn)
        # stacked layout
        self.search_le = SearchLineEdit(30, 12, parent=self)
        self.search_le.setHidden(True)
        # scroll area
        scroll_area = QScrollArea(self)
        self.scroll_central_widget = QWidget(self)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFocusPolicy(Qt.NoFocus)
        scroll_area.setWidget(self.scroll_central_widget)
        # tags layout
        self.tag_layout = QVBoxLayout(self.scroll_central_widget)
        self.tag_layout.setAlignment(Qt.AlignTop)
        self.tag_layout.setContentsMargins(2, 2, 2, 2)
        self.tag_layout.setSpacing(2)
        # button layout
        button_layout = QHBoxLayout()
        self.ok_btn = QPushButton("OK", self)
        self.ok_btn.setFocusPolicy(Qt.NoFocus)
        self.cancel_btn = QPushButton("Cancel", self)
        self.cancel_btn.setFocusPolicy(Qt.NoFocus)
        button_layout.addStretch()
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)
        # add to main layout
        main_layout.addLayout(top_btn_layout)
        main_layout.addWidget(self.search_le)
        main_layout.addWidget(scroll_area)
        main_layout.addLayout(button_layout)
        # set signals
        self.set_signals()

    def set_signals(self):
        """
        信号连接
        :return:
        """
        self.add_tag_btn.clicked.connect(self._show_add_le)
        self.search_tag_btn.clicked.connect(self._show_search_le)
        self.search_le.return_pressed.connect(self.add_tag)
        self.cancel_btn.clicked.connect(self.close)
        self.ok_btn.clicked.connect(self._accept)

    def _show_add_le(self):
        """
        :return:
        """
        self.search_le.setHidden(False)
        self.search_le.setPlaceholderText("New Tag")
        self.search_le.search_button.setIcon(mliber_resource.icon("tag.png"))
        self.search_le.set_completer([])

    def _show_search_le(self):
        """
        :return:
        """
        self.search_le.setHidden(False)
        self.search_le.setPlaceholderText("Search...")
        self.search_le.search_button.setIcon(mliber_resource.icon("search.png"))
        with mliber_global.db() as db:
            tags = db.find("Tag", [])
            tag_names = [tag.name for tag in tags]
            self.set_completer(tag_names)

    @property
    def tag_icon_path(self):
        """
        get tag icon path
        :return:
        """
        return mliber_resource.icon_path("tag.png")

    def add_tag(self, tag_name, color=QColor(138, 138, 138)):
        """
        添加tag
        :param tag_name:
        :param color:
        :return:
        """
        if not tag_name:
            return
        if tag_name in self.exist_tags():
            return
        button = IconButton(self)
        button.setFixedWidth(self.width()*0.95)
        button.setText(tag_name)
        button.set_height(24)
        button.set_icon(mliber_resource.icon("tag.png"))
        button.set_icon_color(color)
        self.tag_layout.addWidget(button)
        self.search_le.setText("")

    def add_tags(self, tag_name_list):
        """
        add tags
        :param tag_name_list: <list>
        :return:
        """
        if not tag_name_list:
            return
        for tag_name in tag_name_list:
            self.add_tag(tag_name)

    def exist_tags(self):
        """
        :return:
        """
        tags = list()
        for i in xrange(self.tag_layout.count()):
            widget = self.tag_layout.itemAt(i).widget()
            if isinstance(widget, QToolButton):
                tags.append(widget.text())
        return tags

    def _accept(self):
        """
        :return:
        """
        tags = self.exist_tags()
        self.ok_clicked.emit(tags)
        self.close()

    def set_completer(self, completer_list):
        """
        set completer
        :return:
        """
        self.search_le.set_completer(completer_list)


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        ctw = CreateTagWidget()
        ctw.show()
