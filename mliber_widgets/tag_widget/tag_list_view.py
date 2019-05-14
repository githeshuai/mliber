# -*- coding:utf-8 -*-
from datetime import datetime
from functools import partial
from Qt.QtWidgets import QListView, QAbstractItemView, QMenu, QAction, QInputDialog, QColorDialog
from Qt.QtCore import Qt, Signal
from Qt.QtGui import QFontMetricsF, QFont, QColor, QCursor
from tag_model import TagModel, TagProxyModel
from tag_delegate import TagDelegate
from mliber_conf import mliber_config
import mliber_global
from mliber_api.database_api import Database

LIST_VIEW_STYLE = "QListView::item{background: #393c46; border-radius: 10px; border: 0px solid;}" \
                  "QListView::item:selected {background: #29475a;}" \
                  "QListView::item:hover {background: #345f71;}"\
                  "QListView::item:selected:!active {background: #0f0;}" \
                  "QListView::item:selected:active {background: #0f0;}"


class TagListItem(object):
    def __init__(self, tag):
        """
        :param tag: <Tag> Tag object
        """
        self.tag = tag
        self.text = self.tag.name
        self.width = self.text_width() + 30
        self.color = QColor(self.tag.colorR or mliber_config.TAG_COLOR_R,
                            self.tag.colorG or mliber_config.TAG_COLOR_G,
                            self.tag.colorB or mliber_config.TAG_COLOR_B)

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
        font = self.font()
        metrics = QFontMetricsF(font)
        return metrics.boundingRect(self.text)

    def text_width(self):
        """
        text width
        :return:
        """
        text_width = self.text_rect().width()
        return max(0, text_width)


class TagListView(QListView):
    selection_changed = Signal(list)

    def __init__(self, parent=None):
        super(TagListView, self).__init__(parent)
        self.tags = []
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
        database = mliber_global.app().value("mliber_database")
        return Database(database)

    @property
    def library(self):
        """
        :return:
        """
        return mliber_global.library()

    @property
    def user(self):
        """
        :return:
        """
        return mliber_global.user()

    @staticmethod
    def _get_model_data(tags):
        """
        获取所有的library
        :param tags: <list> Tag object instance list
        :return:
        """
        model_data = list()
        for tag in tags:
            item = TagListItem(tag)
            model_data.append(item)
        return model_data

    def _set_model(self, tags):
        """
        设置model
        :param tags: <list> Tag object instance list
        :return:
        """
        self.tags = tags
        model_data = self._get_model_data(tags)
        model = TagModel(model_data, self)
        proxy_model = TagProxyModel(self)
        proxy_model.setSourceModel(model)
        self.setModel(proxy_model)
        # selection model
        selection_model = self.selectionModel()
        selection_model.selectionChanged.connect(self._emit_selection_changed)

    def _emit_selection_changed(self):
        """
        :return:
        """
        selected_tags = self.selected_tags()
        self.selection_changed.emit(selected_tags)

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

    def show_data(self, tags):
        """
        show data in list view
        :param tags: <list> Tag object instance list
        :return:
        """
        self._set_model(tags)
        self._set_delegate()

    @property
    def tag_names(self):
        """
        获取当前列表里所有的tag名字
        :return:
        """
        items = self.model().sourceModel().model_data
        return [item.tag.name for item in items]

    def append_tag(self, tag_names, colorR=138, colorG=138, colorB=138):
        """
        添加标签
        :param tag_names: <str>
        :param colorR: <int>
        :param colorG: <int>
        :param colorB: <int>
        :return:
        """
        # 首先判断tag是否在数据库中存在，如果存在不创建
        if isinstance(tag_names, basestring):
            tag_names = [tag_names]
        items = list()
        db = self.db
        for tag_name in tag_names:
            tag = db.find_one("Tag", [["name", "=", tag_name], ["status", "=", "Active"]])
            # tag存在数据库中，但是没有在当前list中，则需要添加进来
            if tag:
                if tag_name not in self.tag_names:
                    item = TagListItem(tag)
                    items.append(item)
            else:
                tag = db.create("Tag", {"name": tag_name, "colorR": colorR, "colorG": colorG,
                                        "colorB": colorB, "created_by": self.user.id})
                item = TagListItem(tag)
                items.append(item)
            # 在ui显示
        if items:
            source_model = self.model().sourceModel()
            self.model().sourceModel().insertRows(source_model.rowCount(), len(items), items)
            self.show_delegate()

    def rename_tag(self, index):
        """
        重命名tag
        :param index: 鼠标右键所在的item的index
        :return:
        """
        # 先修改数据库
        new_name, ok = QInputDialog.getText(self, "New Tag Name", "Input a new tag name")
        if new_name and ok:
            item = self.model().sourceModel().data(index)
            tag_id = item.tag.id
            with mliber_global.db() as db:
                db.update("Tag", tag_id, {"name": new_name,
                                          "updated_by": self.user.id,
                                          "updated_at": datetime.now()})
            # ui显示
            self.model().sourceModel().setData(index, new_name)

    def delete_tag(self):
        """
        删除tag
        :return:
        """
        # 输入密码验证

        selected_tags = self.selected_tags()
        with mliber_global.db() as db:
            for tag in selected_tags:
                db.update("Tag", tag.id, {"status": "Disable",
                                          "updated_by": self.user.id,
                                          "updated_at": datetime.now()})
        # remove in ui
        for index, row in enumerate(self.selected_rows()):
            self.model().sourceModel().removeRows(row-index, 1)

    def change_color(self):
        """
        改变颜色
        :return:
        """
        color_dialog = QColorDialog(self)
        color_dialog.currentColorChanged.connect(self._change_color_in_ui)
        color_dialog.colorSelected.connect(self._change_color_in_database)
        color_dialog.exec_()

    def _change_color_in_ui(self, color):
        """
        改变ui
        :param color: QColor
        :return:
        """
        indexes = self.selected_indexes()
        src_model = self.model().sourceModel()
        for index in indexes:
            src_model.setData(index, color)

    def _change_color_in_database(self, color):
        """

        :param color:
        :return:
        """
        red = int(color.red())
        green = int(color.green())
        blue = int(color.blue())
        selected_tags = self.selected_tags()
        for tag in selected_tags:
            self.db.update("Tag", tag.id, {"colorR": red, "colorG": green, "colorB": blue,
                                           "updated_by": self.user.id,
                                           "updated_at": datetime.now()})

    def selected_indexes(self):
        """
        :return:
        """
        return self.selectedIndexes()

    def selected_rows(self):
        """
        selected rows
        :return:
        """
        selected_indexes = self.selectedIndexes()
        src_indexes = [self.model().mapToSource(index) for index in selected_indexes]
        rows = list(set([index.row() for index in src_indexes]))
        return rows

    def selected_items(self):
        """
        get selected items
        :return:
        """
        items = list()
        for row in self.selected_rows():
            item = self.model().sourceModel().model_data[row]
            items.append(item)
        return items

    def selected_tags(self):
        """
        get selected tags
        :return:
        """
        return [item.tag for item in self.selected_items()]

    def select_all(self):
        """
        select all
        :return:
        """
        self.selectAll()

    def deselect_all(self):
        """
        deselect all
        :return:
        """
        self.clearSelection()

    def contextMenuEvent(self, event):
        """
        右键菜单
        :param event:
        :return:
        """
        if not self.user.tag_permission:
            return
        menu = QMenu(self)
        index = self.indexAt(event.pos())
        if index.row() >= 0:
            src_index = index.model().mapToSource(index)
            rename_action = QAction("Rename", self, triggered=partial(self.rename_tag, src_index))
            menu.addAction(rename_action)
        selected_items = self.selected_items()
        if len(selected_items):
            change_color_action = QAction("Change Color", self, triggered=self.change_color)
            # delete_action = QAction("Delete", self, triggered=self.delete_tag)
            menu.addAction(change_color_action)
            # menu.addAction(delete_action)
        menu.exec_(QCursor.pos())


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        tlv = TagListView()
        tlv.show()
