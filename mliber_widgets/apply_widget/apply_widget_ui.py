# -*- coding:utf-8 -*-
from Qt.QtWidgets import QWidget, QVBoxLayout, QToolButton, QGridLayout, QLabel, QLineEdit, QTextEdit, QHBoxLayout
from Qt.QtCore import Qt
from element_list_view import ElementListView
from mliber_conf import mliber_config


class TitleLabel(QLabel):
    def __init__(self, text, parent=None):
        super(TitleLabel, self).__init__(parent)
        self.setAlignment(Qt.AlignRight)
        self.setText(text)
        self.setMinimumWidth(53)
        self.setStyleSheet("color: #777777")


class TagButton(QToolButton):
    def __init__(self, parent=None):
        super(TagButton, self).__init__(parent)
        style = "background: transparent; padding: 0px; text-decoration: underline; color: %s" % \
                mliber_config.ORANGE_COLOR
        self.setStyleSheet(style)


class TagWidget(QWidget):
    def __init__(self, parent=None):
        super(TagWidget, self).__init__(parent)
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def add_tags(self, tag_names):
        """
        添加tag
        :param tag_names: <list>
        :return:
        """
        for index, tag in enumerate(tag_names):
            row = index / 3
            column = index % 3
            tag_btn = TagButton(self)
            tag_btn.setText(tag)
            self.layout().addWidget(tag_btn, row, column)


class ApplyWidgetUI(QWidget):
    def __init__(self, parent=None):
        super(ApplyWidgetUI, self).__init__(parent)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # thumbnail button
        thumbnail_widget = QWidget(self)
        thumbnail_layout = QHBoxLayout(thumbnail_widget)
        thumbnail_layout.setContentsMargins(0, 0, 0, 0)
        self.thumbnail_widget = QToolButton(self)
        thumbnail_layout.addWidget(self.thumbnail_widget)
        # info layout
        info_layout = QGridLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        id_label = TitleLabel("id", self)
        self.id_le = QLineEdit(self)
        name_label = TitleLabel("name", self)
        self.name_le = QLineEdit(self)
        self.name_le.setReadOnly(True)
        created_by_label = TitleLabel("created by", self)
        self.created_by_le = QLineEdit(self)
        self.created_by_le.setReadOnly(True)
        created_at_label = TitleLabel("created at", self)
        self.created_at_le = QLineEdit(self)
        self.created_at_le.setReadOnly(True)
        tag_label = TitleLabel("tag", self)
        self.tag_widget = TagWidget(self)
        description_label = TitleLabel("description", self)
        self.description_te = QTextEdit(self)
        self.description_te.setReadOnly(True)
        info_layout.addWidget(id_label, 0, 0, 1, 1)
        info_layout.addWidget(self.id_le, 0, 1, 1, 3)
        info_layout.addWidget(name_label, 1, 0, 1, 1)
        info_layout.addWidget(self.name_le, 1, 1, 1, 3)
        info_layout.addWidget(created_by_label, 2, 0, 1, 1)
        info_layout.addWidget(self.created_by_le, 2, 1, 1, 3)
        info_layout.addWidget(created_at_label, 3, 0, 1, 1)
        info_layout.addWidget(self.created_at_le, 3, 1, 1, 3)
        info_layout.addWidget(tag_label, 4, 0, 1, 1)
        info_layout.addWidget(self.tag_widget, 4, 1, 1, 3)
        info_layout.addWidget(description_label, 5, 0, 1, 1)
        info_layout.addWidget(self.description_te, 5, 1, 1, 3)
        # element widget
        self.element_list_view = ElementListView(self)
        # add to main layout
        main_layout.addWidget(thumbnail_widget)
        main_layout.addLayout(info_layout)
        main_layout.addWidget(self.element_list_view)


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        a = ApplyWidgetUI()
        a.show()
