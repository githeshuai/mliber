# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import QListWidget, QAction, QListWidgetItem, QMenu, QFileDialog
from Qt.QtCore import QSize, Qt
from Qt.QtGui import QCursor
import mliber_resource


class FileListWidget(QListWidget):
    def __init__(self, parent=None):
        super(FileListWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setSortingEnabled(True)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.setIconSize(QSize(30, 30))
        self.setFocusPolicy(Qt.NoFocus)

    def remove(self):
        """
        删除选中项
        :return:
        """
        selected_items = self.selectedItems()
        if not selected_items:
            return
        for item in self.selectedItems():
            self.takeItem(self.row(item))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = str(url.toLocalFile())
            self.add_file_item(path)

    def contextMenuEvent(self, event):
        """
        右键菜单
        :param event:
        :return:
        """
        menu = QMenu(self)
        add_action = QAction("Add", self, triggered=self.add_from_local_disk)
        menu.addAction(add_action)
        if self.selectedItems():
            remove_action = QAction("Remove", self, triggered=self.remove)
            menu.addAction(remove_action)
        clear_action = QAction("Clear", self, triggered=self.clear)
        menu.addAction(clear_action)
        menu.exec_(QCursor.pos())
        event.accept()

    def all_items_text(self):
        """
        所有item的text
        :return:
        """
        all_items_text = list()
        if self.count():
            for i in xrange(self.count()):
                try:
                    all_items_text.append(str(self.item(i).text()))
                except Exception as e:
                    print str(e)
            all_items_text = [item.replace("\\", "/") for item in all_items_text]
        return all_items_text

    def append_file(self, file_path):
        """
        添加文件
        :param file_path:
        :return:
        """
        file_path = file_path.replace("\\", "/")
        if file_path.endswith("Thumbs.db"):
            return
        if file_path.endswith(".swatches"):
            return
        exists = self.all_items_text()
        if file_path in exists:
            return
        item = QListWidgetItem(file_path, self)
        item.setSizeHint(QSize(item.sizeHint().width(), 35))
        item.setIcon(mliber_resource.icon("file.png"))
        self.addItem(item)

    def append_dir(self, file_dir):
        """
        添加路径
        :param file_dir:
        :return:
        """
        all_files = list()
        for root, dirs, files in os.walk(file_dir):
            for f in files:
                all_files.append(os.path.join(root, f))
                all_files = [f.replace('\\', '/') for f in all_files]
        if not all_files:
            return
        for file_path in all_files:
            self.append_file(file_path)

    def add_file_item(self, path):
        """
        添加item
        :param path:
        :return:
        """
        if os.path.isfile(path):
            self.append_file(path)
        elif os.path.isdir(path):
            self.append_dir(path)
        else:
            return

    def add_from_local_disk(self):
        """
        选择本地文件添加
        :return:
        """
        files, ok = QFileDialog.getOpenFileNames(self, u"Choose files")
        if ok:
            for f in files:
                self.add_file_item(f)
