# -*- coding:utf-8 -*-
from Qt.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from tag_list_view import TagListView
from mliber_qt_components.search_line_edit import SearchLineEdit
from mliber_qt_components.toolbutton import ToolButton


class TagWidget(QWidget):
    def __init__(self, parent=None):
        super(TagWidget, self).__init__(parent)
        main_layout = QVBoxLayout(self)
        # top layout
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        self.tag_btn = QPushButton("Tag", self)
        self.search_le = SearchLineEdit(22, 12, self)
        self.add_btn = ToolButton(self)
        self.add_btn.set_size()
        self.add_btn.set_icon("add.png")
        top_layout.addWidget(self.tag_btn)
        top_layout.addStretch()
        top_layout.addWidget(self.search_le)
        top_layout.addWidget(self.add_btn)
        # tag list view
        self.tag_list_view = TagListView(self)
        # add to main layout
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.tag_list_view)


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        tw = TagWidget()
        tw.show()

