# -*- coding:utf-8 -*-
from Qt.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMenu, QAction, QDialog, \
    QLabel, QLineEdit, QColorDialog
from tag_list_view import TagListView
import mliber_global
from mliber_qt_components.search_line_edit import SearchLineEdit
from mliber_qt_components.indicator_button import IndicatorButton


class TagWidget(QWidget):
    def __init__(self, parent=None):
        super(TagWidget, self).__init__(parent)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # top layout
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        self.tag_btn = IndicatorButton("Tag", self)
        self.search_le = SearchLineEdit(22, 12, self)
        top_layout.addWidget(self.tag_btn)
        top_layout.addStretch()
        top_layout.addWidget(self.search_le)
        # tag list view
        self.tag_list_view = TagListView(self)
        # add to main layout
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.tag_list_view)
        # set signals
        self._set_signals()
        # create tag menu
        # self._create_tag_menu()

    def _set_signals(self):
        """
        信号连接
        :return:
        """
        self.search_le.text_changed.connect(self._filter)

    @property
    def user(self):
        return mliber_global.user()

    def _create_tag_menu(self):
        """
        创建setting菜单
        :return:
        """
        self.tag_btn.set_menu()
        self.tag_btn.add_menu_action("Select All", self._select_all)
        self.tag_btn.add_menu_action("Deselect All", self.deselect_all)

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

    def deselect_all(self):
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

