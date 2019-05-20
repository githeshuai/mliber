# -*- coding:utf-8 -*-
from Qt.QtWidgets import QListView, QAbstractItemView
from Qt.QtCore import Qt
from element_model import ElementModel
from element_delegate import ElementDelegate
from mliber_conf import mliber_config
import mliber_global


class ElementItem(object):
    def __init__(self, element):
        """
        :param element: <Element>
        """
        self.element = element

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
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        # set style
        self.set_style()

    def set_style(self):
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

    def _get_model_data(self, elements):
        """
        :param elements:
        :return:
        """
        model_data = list()
        for element in elements:
            item = ElementItem(element)
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
