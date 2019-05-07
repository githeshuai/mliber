# -*- coding:utf-8 -*-
from Qt.QtWidgets import QListView, QAbstractItemView
from Qt.QtCore import Qt
from Qt.QtGui import QFontMetricsF, QFont
from tag_model import TagModel, TagProxyModel
from tag_delegate import TagDelegate
from mliber_conf import mliber_config
import mliber_global


LIST_VIEW_STYLE = "QListView::item{background: #393c46; border-radius: 10px; border: 0px solid;}" \
                  "QListView::item:selected {background: #29475a;}" \
                  "QListView::item:hover {background: #345f71;}"\
                  "QListView::item:selected:!active {background: #228B22;}" \
                  "QListView::item:selected:active {background: #228B22;}"


class TagListItem(object):
    def __init__(self):
        self.__text = None
        self.__width = None

    def set_text(self, text):
        """
        :return:
        """
        self.__text = text
        self.__width = self.text_width() + 25

    def text(self):
        """
        :return:
        """
        return self.__text

    def width(self):
        """
        :return:
        """
        return self.__width

    @staticmethod
    def font():
        """
        get font
        :return: QFont
        """
        return QFont(mliber_config.FONT_NAME)

    def text_rect(self):
        """
        :return:
        """
        text = self.text()
        font = self.font()
        metrics = QFontMetricsF(font)
        return metrics.boundingRect(text)

    def text_width(self):
        """
        text width
        :return:
        """
        text_width = self.text_rect().width()
        return max(0, text_width)


class TagListView(QListView):
    def __init__(self, parent=None):
        super(TagListView, self).__init__(parent)
        self.setSpacing(0)
        self.setMouseTracking(True)
        self.setSpacing(2)
        # self.setSelectionRectVisible(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setSelectionMode(QAbstractItemView.MultiSelection)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.set_style()

    def set_style(self):
        """
        set style sheet
        :return:
        """
        self.setStyleSheet(LIST_VIEW_STYLE)

    @property
    def db(self):
        """
        :return:
        """
        return mliber_global.app().value("mliber_database")

    @property
    def library(self):
        """
        :return:
        """
        return mliber_global.app().value("mliber_library")

    @property
    def user(self):
        """
        :return:
        """
        return mliber_global.app().value("mliber_user")

    @staticmethod
    def _get_model_data():
        """
        获取所有的library
        :return:
        """
        model_data = list()
        tags = ["hello", "world", u"我信了你的邪啊", u"顶你个肺", "what the fuck", u"植物", u"花"]
        for tag in tags:
            item = TagListItem()
            item.set_text(tag)
            model_data.append(item)
        return model_data

    def _set_model(self):
        """
        设置model
        :return:
        """
        model_data = self._get_model_data()
        model = TagModel(model_data, self)
        proxy_model = TagProxyModel(self)
        proxy_model.setSourceModel(model)
        self.setModel(proxy_model)

    def _set_delegate(self):
        """
        设置代理
        :return:
        """
        delegate = TagDelegate(self)
        self.setItemDelegate(delegate)
        self.show_delegate()

    def show_delegate(self):
        """
        show delegate
        :return:
        """
        for row in xrange(self.model().rowCount()):
            self.openPersistentEditor(self.model().index(row, 0))

    def show_data(self):
        """
        show data in list view
        :return:
        """
        self._set_model()
        self._set_delegate()

    def add_tag(self, tag_name):
        """
        添加标签
        :return:
        """
        # 首先在数据库里添加tag

        # 在ui显示

    def rename_tag(self):
        """
        重命名tag
        :return:
        """

    def delete_tag(self):
        """
        删除tag
        :return:
        """

    def mousePressEvent(self, event):
        """
        当鼠标点击空白处，取消全部选择
        :return:
        """
        super(TagListView, self).mousePressEvent(event)
        point = event.pos()
        index = self.indexAt(point)
        if index.row() < 0:
            self.clearSelection()


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        tag = TagListView()
        tag.show_data()
        tag.show()
