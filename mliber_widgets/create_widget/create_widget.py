# -*- coding:utf-8 -*-
import logging
from Qt.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QGridLayout, QLineEdit, QTextEdit, QPushButton, \
    QScrollArea, QCheckBox, \
    QButtonGroup, QLayout, QProgressBar
from Qt.QtCore import Qt, Signal
from mliber_parse.library_parser import Library
from mliber_qt_components.thumbnail_widget import ThumbnailWidget
from mliber_qt_components.messagebox import MessageBox
from mliber_qt_components.input_text_edit import InputTextEdit
from mliber_qt_components.action_widget import ActionWidget
import mliber_global
import mliber_resource
from mliber_libs.dcc_libs.dcc import Dcc
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


class CreateWidget(QScrollArea):
    created_signal = Signal(list)
    
    def __init__(self, library_type=None, parent=None):
        super(CreateWidget, self).__init__(parent)
        self._library_type = library_type
        self._engine = Dcc.engine()
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
        # show widgets
        self._show_thumbnail()
        self._show_common()
        self._show_library_widget()
        self._show_actions()
        self._show_frame_range()
        self._show_progress_bar()
        self._show_create_button()
        self._set_signals()

    def _set_signals(self):
        self.asset_name_le.textChanged.connect(self._show_asset_dir)
        self.create_btn.clicked.connect(self._on_create_btn_clicked)
        
    def _show_thumbnail(self):
        """
        insert thumbnail widget
        Returns:
        """
        self.thumbnail_widget = ThumbnailWidget(self)
        self.main_layout.addWidget(self.thumbnail_widget)

    def _show_common(self):
        """
        common widget: include name、tag、 comment。。。。。
        Returns:
        """
        layout = QGridLayout()
        name_label = TitleLabel("Name", True, parent=self)
        # asset name line edit
        self.asset_name_le = QLineEdit(self)
        self.asset_name_le.setPlaceholderText("asset name")
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
        self.tag_le.setPlaceholderText(u"多个tag，以逗号隔开")
        # 描述label
        comment_label = TitleLabel("Comment", False, self)
        self.comment_tx = QTextEdit(self)
        self.comment_tx.setMinimumHeight(60)
        blank_label = QLabel(self)
        self.overwrite_check_box = QCheckBox("Overwrite", self)
        self.overwrite_check_box.setChecked(True)
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

    def _show_library_widget(self):
        """
        :return:
        """
        library_widget = self.create_library_widget()
        if library_widget:
            self.main_layout.addWidget(library_widget)

    def _show_actions(self):
        """
        从library.yml中读取信息， 创建checkbox widget
        Returns:
        """
        engine = self._engine
        print engine
        self.actions_widget = ActionWidget(self._library_type, engine, self)
        self.main_layout.addWidget(self.actions_widget)

    def _show_frame_range(self):
        """
        创建frame range layout
        Returns: QVBoxLayout
        """
        if Library(self._library_type).show_frame_range():
            frame_range_layout = QVBoxLayout()
            frame_range_layout.setContentsMargins(0, 0, 0, 0)
            fr_label = QLabel(self)
            fr_label.setText("<font color=#fff size=4><b>Frame Range</b></font>")
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

    def _show_progress_bar(self):
        """
        显示进度条
        :return:
        """
        self.progress_bar = QProgressBar(self)
        self.progress_bar.hide()
        self.progress_bar.setTextVisible(False)
        self.main_layout.addWidget(self.progress_bar)

    def _show_create_button(self):
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
        """
        当前选中的category
        :return:
        """
        categories = mliber_global.categories()
        if categories and len(categories) == 1:
            return categories[0]

    @property
    def category_dir(self):
        """
        当前category路径
        :return:
        """
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
        """
        资产名字
        :return:
        """
        return self.asset_name_le.text()

    @property
    def asset_dir(self):
        """
        资产路径
        :return:
        """
        category_dir = self.category_dir
        if category_dir:
            return Path(category_dir).join(self.asset_name)
        return ""

    @property
    def start(self):
        """
        起始帧
        :return:
        """
        if hasattr(self, "start_le"):
            return int(self.start_le.text())
        return 1

    @property
    def end(self):
        """
        结束帧
        :return:
        """
        if hasattr(self, "end_le"):
            return int(self.end_le.text())
        return 1

    @property
    def description(self):
        """
        描述
        :return:
        """
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

    def _show_asset_dir(self):
        """
        显示资产将要存放的路径
        Returns:
        """
        self.asset_dir_te.setText(self.asset_dir)

    def _on_create_btn_clicked(self):
        """
        create按钮按下的时候，执行的操作
        :return:
        """
        if all((self.thumbnail_files, self.asset_dir, self.asset_name, self.library, self.category, self.types)):
            if self.preflight():
                self.run()
        else:
            MessageBox.warning(self, "Warning", u"[thumbnail, library, category, asset name, actions] necessary。")

    def preflight(self):
        """
        检查项
        :return:
        """
        return True

    def run(self):
        """
        点击create按钮运行的函数，子类需要继承需要重写
        Returns:
        """
        if Library(self._library_type).need_check_selected():
            text_edit = InputTextEdit(self)
            text_edit.set_title("Selected Nodes")
            text_edit.set_data(Dcc(self._engine).selected_object_names())
            text_edit.editTextFinished.connect(self.start_create)
            text_edit.exec_()
        else:
            self.start_create()

    def start_create(self):
        """
        :return:
        """
        objects = list()
        if Library(self._library_type).need_check_selected():
            objects = Dcc(self._engine).selected_objects()
            if not objects:
                MessageBox.warning(self, "Warning", "No objects selected.")
                return
        from mliber_api.asset_maker import AssetMaker
        # database_name, library_id, category_id, asset_name, objects, types = list(), start = 1, end = 1,
        # thumbnail_files = list(), tag_names = list(), description = "", overwrite = True, created_by = None
        data = dict(database_name=self.database,
                    library_id=self.library.id,
                    category_id=self.category.id,
                    asset_name=self.asset_name,
                    objects=objects,
                    types=self.types,
                    start=self.start,
                    end=self.end,
                    thumbnail_files=self.thumbnail_files,
                    tag_names=self.tags,
                    description=self.description,
                    overwrite=self.overwrite,
                    created_by=self.user.id)
        self.progress_bar.show()
        self.progress_bar.setRange(0, 10)
        self.progress_bar.setValue(6)
        try:
            asset_maker = AssetMaker(**data)
            asset = asset_maker.make()
            if asset:
                self.created_signal.emit([asset])
        except Exception as e:
            logging.error(str(e))
            MessageBox.warning(self, "Code Error", str(e))
        finally:
            self.progress_bar.setValue(10)
            self.progress_bar.hide()
