# -*- coding:utf-8 -*-
from Qt.QtWidgets import QListView, QAbstractItemView, QMenu, QAction
from Qt.QtCore import Qt
from Qt.QtGui import QCursor
from element_model import ElementModel
from element_delegate import ElementDelegate
from mliber_conf import mliber_config
import mliber_global
import mliber_resource
from mliber_libs.os_libs.path import Path
from mliber_qt_components.delete_widget import DeleteWidget
from mliber_qt_components.messagebox import MessageBox


class ElementItem(object):
    def __init__(self, element, asset_name):
        """
        :param element: <Element>
        """
        self.element = element
        self.asset_name = asset_name

    def __getattr__(self, item):
        """
        :param item:
        :return:
        """
        if item == "path":
            library = mliber_global.library()
            root_path = library.root_path()
            return self.element.path.format(root=root_path)
        return getattr(self.element, item)


class ElementListView(QListView):
    def __init__(self, parent=None):
        super(ElementListView, self).__init__(parent)
        self._asset = None
        self.setMouseTracking(True)
        self.setSpacing(4)
        self.setSelectionRectVisible(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setResizeMode(QListView.Adjust)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        # set style
        self._set_style()
        # set signals
        self._set_signals()

    def _set_signals(self):
        """
        信号连接
        :return:
        """
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

    def _set_style(self):
        """
        set style
        :return:
        """
        self.setStyleSheet(mliber_config.LIST_VIEW_STYLE)

    def set_asset(self, asset):
        """
        :param asset: <Asset>
        :return:
        """
        self._asset = asset

    def _selected_indexes(self):
        """
        获取选择的index
        :return:
        """
        selected_indexes = self.selectedIndexes()
        return selected_indexes

    def _selected_rows(self):
        """
        获取选择的行
        :return:
        """
        selected_indexes = self._selected_indexes()
        rows = list(set([index.row() for index in selected_indexes]))
        return rows

    def _show_context_menu(self):
        """
        显示右键菜单
        :return:
        """
        rows = self._selected_rows()
        if not rows:
            return
        menu = QMenu(self)
        delete_action = QAction(mliber_resource.icon("delete.png"), "Send to Trash", self, triggered=self._show_delete_widget)
        menu.addAction(delete_action)
        menu.exec_(QCursor.pos())

    def _show_delete_widget(self):
        """
        :return:
        """
        delete_widget = DeleteWidget(self)
        delete_widget.accept_signal.connect(self._delete_element)
        delete_widget.exec_()

    def _delete_element(self, delete_source):
        """
        删除element
        :return:
        """
        row = self._selected_rows()[0]
        item = self.model().model_data[row]
        element = item.element
        with mliber_global.db() as db:
            db.update("Element", element.id, {"status": "Disable"})
        self.model().removeRows(row, 1)
        if delete_source:
            try:
                Path(item.path).remove()
            except WindowsError as e:
                print str(e)
                MessageBox.warning(self, "Warning", "Storage files delete Failed，Please delete it manual.")

    def _get_model_data(self, elements):
        """
        :param elements:
        :return:
        """
        model_data = list()
        for element in elements:
            item = ElementItem(element, self._asset.name)
            model_data.append(item)
        return model_data

    def set_elements(self, elements):
        """
        接口
        :param elements: <list> [Element, Element]
        :return:
        """
        model_data = self._get_model_data(elements)
        model = ElementModel(model_data, self)
        self.setModel(model)
        self._set_delegate()

    def _set_delegate(self):
        """
        设置代理
        :return:
        """
        delegate = ElementDelegate(self)
        delegate.set_model(self.model())
        self.setItemDelegate(delegate)
        self.show_delegate()

    def show_delegate(self):
        """
        show delegate
        :return:
        """
        for row in xrange(self.model().rowCount()):
            self.openPersistentEditor(self.model().index(row, 0))

    def mousePressEvent(self, event):
        """
        当鼠标左键点击到空白处，取消选择
        :param event:
        :return:
        """
        super(ElementListView, self).mousePressEvent(event)
        point = event.pos()
        index = self.indexAt(point)
        if index.row() < 0:
            self.clearSelection()
