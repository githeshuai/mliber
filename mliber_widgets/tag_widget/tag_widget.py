# -*- coding:utf-8 -*-
from Qt.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMenu, QAction, QDialog, \
    QLabel, QLineEdit, QColorDialog
from Qt.QtGui import QColor
from Qt.QtCore import Signal
from tag_list_view import TagListView
import mliber_global
from mliber_qt_components.search_line_edit import SearchLineEdit
from mliber_qt_components.toolbutton import ToolButton
from mliber_conf import mliber_config


class AddTagWidget(QDialog):
    ok_clicked = Signal(list)

    def __init__(self, parent=None):
        super(AddTagWidget, self).__init__(parent)
        self.resize(300, 200)
        self.color = QColor(mliber_config.TAG_COLOR_R, mliber_config.TAG_COLOR_G, mliber_config.TAG_COLOR_B)
        self.setWindowTitle("Add Tag")
        main_layout = QVBoxLayout(self)
        # name layout
        name_layout = QHBoxLayout()
        name_layout.setContentsMargins(0, 0, 0, 0)
        name_label = QLabel("name", self)
        name_label.setMaximumWidth(40)
        self.name_le = QLineEdit(self)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_le)
        # color button
        self.color_button = QPushButton("choose color", self)
        # button layout
        button_layout = QHBoxLayout()
        self.ok_btn = QPushButton("Ok", self)
        self.cancel_btn = QPushButton("Cancel", self)
        button_layout.addStretch()
        button_layout.addWidget(self.ok_btn)
        button_layout.addWidget(self.cancel_btn)
        # add to main layout
        main_layout.addLayout(name_layout)
        main_layout.addWidget(self.color_button)
        main_layout.addLayout(button_layout)
        # set signals
        self.set_signals()

    def set_signals(self):
        """
        :return:
        """
        self.color_button.clicked.connect(self.choose_color)
        self.ok_btn.clicked.connect(self.on_ok_clicked)
        self.cancel_btn.clicked.connect(self.close)

    @property
    def name(self):
        return self.name_le.text()

    def choose_color(self):
        """
        选择颜色
        :return:
        """
        color_dialog = QColorDialog(self)
        color_dialog.colorSelected.connect(self.set_color)
        color_dialog.currentColorChanged.connect(self.set_color)
        color_dialog.exec_()

    def set_color(self, color):
        """
        set color
        :param color:
        :return:
        """
        self.color = color
        color_r = color.red()
        color_g = color.green()
        color_b = color.blue()
        self.color_button.setStyleSheet("background: rgb(%s, %s, %s)" % (color_r, color_g, color_b))

    def on_ok_clicked(self):
        """
        :return:
        """
        if not self.name:
            return
        self.ok_clicked.emit([self.name, self.color])


class TagWidget(QWidget):
    def __init__(self, parent=None):
        super(TagWidget, self).__init__(parent)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # top layout
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        self.tag_btn = QPushButton("Tag", self)
        self.search_le = SearchLineEdit(22, 12, self)
        self.refresh_btn = ToolButton(self)
        self.refresh_btn.set_size()
        self.refresh_btn.set_icon("refresh.png")
        top_layout.addWidget(self.tag_btn)
        top_layout.addStretch()
        top_layout.addWidget(self.search_le)
        top_layout.addWidget(self.refresh_btn)
        # tag list view
        self.tag_list_view = TagListView(self)
        # add to main layout
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.tag_list_view)
        # set signals
        self.set_signals()

    def set_signals(self):
        """
        信号连接
        :return:
        """
        self.tag_btn.clicked.connect(self._show_tag_menu)
        self.search_le.text_changed.connect(self._filter)

    @property
    def user(self):
        return mliber_global.user()

    def _create_tag_menu(self):
        """
        创建setting菜单
        :return:
        """
        menu = QMenu(self)
        if self.user.tag_permission:
            add_tag_action = QAction("Add Tag", self, triggered=self._show_add_tag_widget)
            menu.addAction(add_tag_action)
        select_all_action = QAction("Select All", self, triggered=self._select_all)
        deselect_all_action = QAction("Deselect All", self, triggered=self._deselect_all)
        menu.addSeparator()
        menu.addAction(select_all_action)
        menu.addAction(deselect_all_action)
        return menu

    def _show_tag_menu(self):
        """
        显示settings菜单
        :return:
        """
        menu = self._create_tag_menu()
        point = self.tag_btn.rect().bottomLeft()
        point = self.tag_btn.mapToGlobal(point)
        menu.exec_(point)

    def _show_add_tag_widget(self):
        """
        :return:
        """
        self.add_tag_widget = AddTagWidget(self)
        self.add_tag_widget.ok_clicked.connect(self._add_tag)
        self.add_tag_widget.exec_()

    def _add_tag(self, arg):
        """
        添加tag
        :return:
        """
        name, color = arg
        color_r = color.red()
        color_g = color.green()
        color_b = color.blue()
        self.tag_list_view.append_tag(name, color_r, color_g, color_b)
        self.add_tag_widget.accept()

    def _select_all(self):
        """
        选择所有
        :return:
        """
        self.tag_list_view.select_all()

    def _deselect_all(self):
        """
        取消选择
        :return:
        """
        self.tag_list_view.deselect_all()

    def set_tags(self, tags):
        """
        接口
        :param tags: <list>
        :return:
        """
        self.tag_list_view.show_data(tags)
        self.search_le.setText("")
        # set completer
        self.set_completer(self.tag_list_view.tag_names)

    def set_completer(self, tag_list):
        """
        set completer
        :param tag_list: <list>
        :return:
        """
        self.search_le.set_completer(tag_list)

    def _filter(self, filter_str):
        """
        筛选
        :param filter_str:
        :return:
        """
        self.tag_list_view.model().set_filter(filter_str)
        self.tag_list_view.show_delegate()

    def clear(self):
        """
        clear list view
        :return:
        """
        model = self.tag_list_view.model()
        if model:
            model.sourceModel().remove_all()
            self.search_le.setText("")


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        tw = TagWidget()
        tw.show()

