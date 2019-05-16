# -*- coding:utf-8 -*-
from Qt.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QGridLayout, QLineEdit, QDialog, \
    QTextEdit, QComboBox, QApplication, QPushButton, QFileDialog, QCompleter, QScrollArea, QCheckBox, \
    QButtonGroup, QSizePolicy, QLayout, QProgressBar, QMenu, QWidgetAction
from Qt.QtCore import Qt, Signal
from mliber_parse.library_parser import Library
from mliber_qt_components.thumbnail_widget import ThumbnailWidget
from mliber_qt_components.messagebox import MessageBox
import mliber_global
import mliber_resource
from mliber_api.database_api import Database
from mliber_libs.os_libs.path import Path
from mliber_conf import templates


class TitleLabel(QLabel):
    def __init__(self, text, must=False, parent=None):
        super(TitleLabel, self).__init__(parent)
        self.setAlignment(Qt.AlignRight)
        self.name = text
        if must:
            self.set_must()
        else:
            self.setText(self.name)
        self.setMinimumWidth(53)
        self.setStyleSheet("color: #777777")

    def set_must(self):
        """
        设置为必填
        Returns:
        """
        text = self.name
        new_text = "<font color=#f00>*</font>%s" % text
        self.setText(new_text)


class ActionWidget(QWidget):
    """
    根据配置信息显示check box
    """
    def __init__(self, library_type, parent=None):
        super(ActionWidget, self).__init__(parent)
        self.library_type = library_type
        # self settings
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # actions label
        action_label = QLabel("Actions")
        main_layout.addWidget(action_label)
        # scroll area
        scroll_area = QScrollArea(self)
        scroll_area.setMinimumHeight(150)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFocusPolicy(Qt.NoFocus)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # set widget
        widget = QWidget(self)
        self.scroll_layout = QVBoxLayout(widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_layout.setContentsMargins(20, 0, 0, 0)
        self.scroll_layout.setSpacing(5)
        scroll_area.setWidget(widget)
        # add checkboxes
        self.action_btngrp = QButtonGroup()
        self.action_btngrp.setExclusive(False)
        check_box_list = self.create_checkboxes()
        for check_box in check_box_list:
            self.action_btngrp.addButton(check_box)
            self.scroll_layout.addWidget(check_box)
        main_layout.addWidget(scroll_area)

    def action_objects(self):
        """
        get all actions from configuration file
        Returns:
        """
        return Library(self.library_type).actions()

    def create_checkboxes(self):
        """
        create actions
        Returns:list of QCheckBox
        """
        checkbox_list = list()
        action_objects = self.action_objects()
        if action_objects:
            for action_object in action_objects:
                name = action_object.name
                typ = action_object.type
                checked = action_object.checked
                check_box = QCheckBox(name, self)
                check_box.setChecked(checked)
                check_box.type = typ
                checkbox_list.append(check_box)
        return checkbox_list

    def checked_buttons(self):
        """
        获取
        :return:
        """
        return [button for button in self.action_btngrp.buttons() if button.isChecked()]


class CreateWidget(QScrollArea):
    created_signal = Signal(list)

    def __init__(self, library_type=None, parent=None):
        super(CreateWidget, self).__init__(parent)
        self.library_type = library_type
        self.setStyleSheet("border: 0px solid;")
        # main widget
        widget = QWidget(self)
        self.setWidget(widget)
        self.setWidgetResizable(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # main layout
        self.main_layout = QVBoxLayout(widget)
        self.main_layout.setSizeConstraint(QLayout.SetMinimumSize)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

    def set_signals(self):
        self.asset_name_le.textChanged.connect(self.show_asset_dir)
        self.create_btn.clicked.connect(self.on_create_btn_clicked)

    def show_thumbnail(self):
        """
        insert thumbnail widget
        Returns:
        """
        self.thumbnail_widget = ThumbnailWidget(self)
        self.main_layout.addWidget(self.thumbnail_widget)

    def show_common(self):
        """
        common widget: include name、tag、 comment。。。。。
        Returns:
        """
        layout = QGridLayout()
        name_label = TitleLabel("Name", True, parent=self)
        # asset name line edit
        self.asset_name_le = QLineEdit(self)
        self.asset_name_le.setPlaceholderText(u"资产名字，不要有特殊字符。")
        # 显示路径的label
        path_label = QLabel(self)
        path_label.setPixmap(mliber_resource.pixmap("info.png"))
        path_label.setAlignment(Qt.AlignRight)
        self.asset_dir_te = QTextEdit(self)
        self.asset_dir_te.setFocusPolicy(Qt.NoFocus)
        self.asset_dir_te.setReadOnly(True)
        self.asset_dir_te.setFixedHeight(50)
        # tag
        tag_label = TitleLabel("Tag", False, self)
        tag_label.setAlignment(Qt.AlignRight)
        self.tag_le = QLineEdit(self)
        # 描述label
        comment_label = TitleLabel("Comment", False, self)
        self.comment_tx = QTextEdit(self)
        self.comment_tx.setMinimumHeight(60)
        blank_label = QLabel(self)
        self.overwrite_check_box = QCheckBox("Overwrite", self)
        layout.addWidget(name_label, 1, 0, 1, 1)
        layout.addWidget(self.asset_name_le, 1, 1, 1, 4)
        layout.addWidget(path_label, 2, 0, 1, 1)
        layout.addWidget(self.asset_dir_te, 2, 1, 1, 4)
        layout.addWidget(tag_label, 3, 0, 1, 1)
        layout.addWidget(self.tag_le, 3, 1, 1, 4)
        layout.addWidget(comment_label, 4, 0, 1, 1)
        layout.addWidget(self.comment_tx, 4, 1, 1, 4)
        layout.addWidget(blank_label, 5, 0, 1, 1)
        layout.addWidget(self.overwrite_check_box, 5, 1, 1, 4)
        layout.setColumnStretch(0, 0)
        layout.setColumnStretch(1, 1)
        self.main_layout.addLayout(layout)

    def create_library_widget(self):
        """
        根据不同的library,创建不同的widget，子类需要继承重写，返回一个QWidget
        Returns:QWidget
        """
        return None

    def show_library_widget(self):
        """
        :return:
        """
        library_widget = self.create_library_widget()
        if library_widget:
            self.main_layout.addWidget(library_widget)

    def show_actions(self):
        """
        从library.yml中读取信息， 创建checkbox widget
        Returns:
        """
        self.actions_widget = ActionWidget(self.library_type, self)
        self.main_layout.addWidget(self.actions_widget)

    def show_frame_range(self):
        """
        创建frame range layout
        Returns: QVBoxLayout
        """
        frame_range_layout = QVBoxLayout()
        frame_range_layout.setContentsMargins(0, 0, 0, 0)
        fr_label = QLabel("Frame Range")
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        start_label = QLabel("Start")
        self.start_le = QLineEdit()
        self.start_le.setText("1")
        end_label = QLabel("End")
        self.end_le = QLineEdit()
        self.end_le.setText("1")
        h_layout.addWidget(start_label)
        h_layout.addWidget(self.start_le)
        h_layout.addWidget(end_label)
        h_layout.addWidget(self.end_le)
        h_layout.setSpacing(0)
        frame_range_layout.addWidget(fr_label)
        frame_range_layout.addLayout(h_layout)
        frame_range_layout.setSpacing(5)
        self.main_layout.addLayout(frame_range_layout)

    def show_progress_bar(self):
        self.progress_bar = QProgressBar(self)
        self.progress_bar.hide()
        self.progress_bar.setTextVisible(False)
        self.main_layout.addWidget(self.progress_bar)

    def show_create_button(self):
        """
        显示create button
        :return:
        """
        self.create_btn = QPushButton("Create", self)
        self.main_layout.addWidget(self.create_btn)

    @property
    def database(self):
        """
        配置文件中database name
        :return:
        """
        database = mliber_global.app().value("mliber_database")
        return database

    @property
    def db(self):
        return Database(self.database)

    @property
    def user(self):
        """
        当前用户
        :return:
        """
        return mliber_global.user()

    @property
    def library(self):
        """
        全局library
        :return:
        """
        return mliber_global.library()

    @property
    def library_dir(self):
        """
        library路径
        :return:
        """
        return self.library.root_path()

    @property
    def category(self):
        categories = mliber_global.categories()
        if categories and len(categories) == 1:
            return categories[0]

    @property
    def category_dir(self):
        category = self.category
        if category:
            return category.path.format(root=self.library_dir)

    @property
    def tags(self):
        tag_str = self.tag_le.text()
        if tag_str:
            return tag_str.split(",")
        return []

    @property
    def thumbnail_files(self):
        """
        用户在thumbnail widget里添加的数据
        :return:
        """
        return self.thumbnail_widget.files()

    @property
    def thumbnail_path(self):
        """
        最终要存放的缩略图路径
        :return:
        """
        thumbnail_format = templates.THUMBNAIL_PATH
        return thumbnail_format.format(self.asset_dir, self.asset_name)

    @property
    def asset_name(self):
        return self.asset_name_le.text()

    @property
    def asset_dir(self):
        category_dir = self.category_dir
        if category_dir:
            return Path(category_dir).join(self.asset_name)
        return ""

    @property
    def start(self):
        return int(self.start_le.text())

    @property
    def end(self):
        return int(self.end_le.text())

    @property
    def description(self):
        return self.comment_tx.toPlainText()

    @property
    def overwrite(self):
        """
        是否覆盖
        :return:
        """
        return self.overwrite_check_box.isChecked()

    @property
    def types(self):
        """
        勾选的action
        :return:
        """
        checked_buttons = self.actions_widget.checked_buttons()
        types = [checked_button.type for checked_button in checked_buttons]
        return types

    def show_asset_dir(self):
        """
        显示资产将要存放的路径
        Returns:
        """
        self.asset_dir_te.setText(self.asset_dir)

    def create_thumbnail(self):
        """
        创建缩略图
        Returns:
        """
        self.thumbnail_widget.convert_to(self.thumbnail_path)

    def on_create_btn_clicked(self):
        """
        create按钮按下的时候，执行的操作
        :return:
        """
        if all((self.asset_dir, self.asset_name, self.library, self.category, self.types)):
            if self.preflight():
                self.run()
        else:
            MessageBox.warning(self, "Warning", u"必填项[library,category,asset name, actions]内容未填。")

    def preflight(self):
        """
        在运行之前，检查是否合法
        :return:
        """
        return True

    def run(self):
        """
        点击create按钮运行的函数，子类需要继承需要重写
        Returns:
        """
        return


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        s = CreateWidget("MayaAsset")
        s.show_thumbnail()
        s.show_actions()
        s.show_frame_range()
        s.show()
