# -*- coding:utf-8 -*-
from functools import partial
from Qt.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QToolButton, QStyledItemDelegate
from Qt.QtGui import QColor, QIcon, QPixmap
from Qt.QtCore import QSize, Qt, Signal, QModelIndex
from mliber_qt_components.icon import Icon
from mliber_qt_components.image_sequence_widget import ImageSequenceWidget
import mliber_resource

FONT_HEIGHT = 18
DEFAULT_COLOR = QColor(138, 138, 138)


class FlagWidget(QToolButton):
    def __init__(self, parent=None):
        super(FlagWidget, self).__init__(parent)
        self.setStyleSheet("border: 0px solid; padding: 0px; background: transparent;")
        self.set_icon_size(QSize(15, 15))

    def set_icon(self, icon_path, icon_color=DEFAULT_COLOR):
        """
        set icon
        :param icon_path: <str>
        :param icon_color: QColor
        :return:
        """
        icon = Icon(icon_path)
        icon.set_color(icon_color)
        self.setIcon(icon)

    def set_icon_color(self, icon_color):
        """
        :param icon_color: QColor
        :return:
        """
        icon = Icon(self.icon())
        icon.set_color(icon_color)
        self.setIcon(icon)

    def set_icon_size(self, size):
        """
        set icon label size
        :param size:
        :return:
        """
        self.setIconSize(size)
        self.setFixedSize(size)


class CellAssetWidget(QWidget):
    def __init__(self, parent=None):
        super(CellAssetWidget, self).__init__(parent)
        self.setAutoFillBackground(True)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(3, 0, 3, 0)
        # flag layout
        flag_layout = QHBoxLayout()
        flag_layout.setAlignment(Qt.AlignLeft)
        flag_layout.setContentsMargins(0, 2, 0, 0)
        self.tag_flag = FlagWidget(self)
        self.tag_flag.set_icon(mliber_resource.icon_path("tag.png"))
        self.store_flag = FlagWidget(self)
        self.store_flag.set_icon(mliber_resource.icon_path("store.png"))
        self.description_flag = FlagWidget(self)
        self.description_flag.set_icon(mliber_resource.icon_path("description.png"))
        flag_layout.addWidget(self.tag_flag)
        flag_layout.addWidget(self.store_flag)
        flag_layout.addWidget(self.description_flag)
        # central icon widget
        self.icon_widget = ImageSequenceWidget(self)
        # text label
        self.name_label = QLabel(self)
        self.name_label.setStyleSheet("background: transparent;")
        self.name_label.setMaximumHeight(FONT_HEIGHT)
        self.name_label.setAlignment(Qt.AlignCenter)
        # add to main layout
        main_layout.addLayout(flag_layout)
        main_layout.addWidget(self.icon_widget)
        main_layout.addWidget(self.name_label)
        main_layout.setSpacing(2)

    def light_tag_flag(self, color):
        """
        点亮tag flag - -
        :param color: QColor
        :return:
        """
        self.tag_flag.set_icon_color(color)

    def light_store_flag(self, color):
        """
        点亮收藏flag
        :param color: QColor
        :return:
        """
        self.store_flag.set_icon_color(color)

    def dark_store_flag(self):
        """
        取消点亮
        :return:
        """
        self.store_flag.set_icon_color(DEFAULT_COLOR)

    def light_description_flag(self, color):
        """
        点亮description flag
        :param color:
        :return:
        """
        self.description_flag.set_icon_color(color)

    def set_name(self, text):
        """
        set text
        :return:
        """
        self.name_label.setText("<font size=4><b>%s</b></font>" % text)

    def set_icon(self, icon_path):
        """
        设置显示图片
        :return:
        """
        self.icon_widget.setDirname(icon_path)

    def set_icon_size(self, size):
        """
        set icon label size
        :param size:
        :return:
        """
        self.icon_widget.setSize(size)

    def set_view(self, view):
        """
        set parent view
        :param view: QListView
        :return:
        """
        self.icon_widget.setView(view)


class AssetDelegate(QStyledItemDelegate):
    store_clicked = Signal(QModelIndex)

    def __init__(self, parent=None):
        super(AssetDelegate, self).__init__(parent)
        self.__parent = parent
        self.__model = self.__parent.model()
        self.__source_model = self.__model.sourceModel()

    def createEditor(self, parent, option, index):
        editor = CellAssetWidget(parent)
        editor.set_view(self.__parent)
        editor.store_flag.clicked.connect(partial(self.store_clicked.emit, index))
        return editor

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        item = self._get_item(index)
        editor.set_icon_size(item.icon_size)
        # image = self.__parent.image_server.get_image(item.icon_path)
        # if image:
        #     editor.set_icon(QIcon(QPixmap.fromImage(image)))
        editor.set_icon(item.icon_path)
        editor.set_name(item.name)
        if item.has_tag:
            editor.light_tag_flag(QColor(50, 100, 255))
        if item.has_description:
            editor.light_description_flag(QColor(50, 255, 100))
        if item.stored_by_me:
            editor.light_store_flag(QColor(255, 100, 50))
        else:
            editor.dark_store_flag()
        editor.blockSignals(False)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def sizeHint(self, option, index):
        item = self._get_item(index)
        size = QSize(item.icon_size.width()+6, item.icon_size.height()+FONT_HEIGHT*2)
        return size
    
    def _get_source_index(self, index):
        """
        获取source index
        :return: 
        """
        source_index = self.__model.mapToSource(index)
        return source_index

    def _get_item(self, index):
        """
        get source index
        :param index:
        :return:
        """
        source_index = self._get_source_index(index)
        item = self.__source_model.data(source_index, Qt.UserRole)
        return item
