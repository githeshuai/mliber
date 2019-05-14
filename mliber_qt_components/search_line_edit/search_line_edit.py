# -*- coding: utf-8 -*-
import os
from Qt.QtWidgets import QLineEdit, QApplication, QToolButton, QStyle, QMenu, QAction, QActionGroup, QCompleter
from Qt.QtGui import QPixmap, QPainter, QIcon, QStandardItemModel, QStandardItem
from Qt.QtCore import Qt, QSize, Signal


class SearchLineEdit(QLineEdit):
    text_changed = Signal(basestring)
    return_pressed = Signal(basestring)

    def __init__(self, height=30, font_size=14, parent=None):
        """
        Args:
            height: <int>
            font_size: <int>
            parent:
        Returns:
        """
        super(SearchLineEdit, self).__init__(parent)
        self.setPlaceholderText("search...")
        self.search_list = []
        self.menu = QMenu(self)
        self.search_icon_path = self.get_icon("search.png")
        self.clear_icon_path = self.get_icon("clear.png")
        self.font_size = font_size
        self.setFixedHeight(height)
        # search pixmap
        self.search_button = self.create_button(self.search_icon_path)
        # right clear button
        self.clear_button = self.create_button(self.clear_icon_path)
        self.clear_button.setVisible(False)
        # self settings
        self.set_style()
        # signals
        self.build_connections()
        
    def set_style(self):
        frame_width = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        clear_button_size = self.clear_button.sizeHint()
        self.setMinimumSize(max(self.minimumSizeHint().width(), clear_button_size.width() + frame_width*2 + 2),
                            max(self.minimumSizeHint().height(), clear_button_size.height() + frame_width*2 + 2))
        style_sheet = "QLineEdit{border: 1px solid #333;border-radius: %spx; " \
                      "padding-right: %dpx;padding-left: %dpx;" \
                      "font-size: %dpx; font-family: Arial;}" \
                      % (self.height()/2, clear_button_size.width() + frame_width + 1,
                         self.search_button.width() + 5, self.font_size)
        self.setStyleSheet(style_sheet)

    @staticmethod
    def get_icon(icon_name):
        icon_path = os.path.join(__file__, "..", icon_name)
        icon_path = os.path.abspath(icon_path).replace("\\", "/")
        return icon_path

    def build_connections(self):
        """
        signal connections
        Returns:
        """
        self.search_button.clicked.connect(self.show_search_menu)
        self.clear_button.clicked.connect(self.on_clear_button_clicked)
        self.textChanged.connect(self.on_text_changed)
        self.returnPressed.connect(self.refresh_history)

    def create_button(self, icon_path):
        """
        create button
        Args:
            icon_path: <str> an icon file path
        Returns:
        """
        button = QToolButton(self)
        button_size = QSize(self.height()*0.6, self.height()*0.6)
        button.setFixedSize(button_size)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(button.size().width()-2, button.size().height()-2))
        button.setStyleSheet('border: 0px; padding: 0px; background: transparent;')
        button.setCursor(Qt.ArrowCursor)
        return button

    def on_text_changed(self, text):
        """
        on text changed
        Args:
            text: lineEdit里的内容
        Returns:

        """
        self.clear_button.setVisible(bool(self.text()))
        self.text_changed.emit(text)

    def refresh_history(self):
        """
        on return pressed
        Returns:
        """
        text = self.text()
        if text not in self.search_list:
            if len(self.search_list) > 10:
                self.search_list.pop(-1)
            self.search_list.insert(0, text)
        self.return_pressed.emit(self.text())

    def on_clear_button_clicked(self):
        """
        on clear button clicked
        Returns:
        """
        self.clear()
        self.return_pressed.emit(self.text())

    def show_search_menu(self):
        """
        show search history menu
        Returns:
        """
        if not self.search_list:
            return
        self.menu.clear()
        action_group = QActionGroup(self)
        for name in self.search_list:
            action = action_group.addAction(name)
            self.menu.addAction(action)
        action_group.triggered.connect(self.set_text)
        point = self.search_button.rect().bottomLeft()
        point = self.search_button.mapToGlobal(point)
        x = point.x() - 10
        point.setX(x)
        self.menu.exec_(point)

    def set_text(self, action):
        """
        on action triggered
        Args:
            action: QAction
        Returns:
        """
        text = action.text()
        self.setText(text)

    def resizeEvent(self, event):
        clear_button_size = self.clear_button.sizeHint()
        frame_width = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        self.search_button.move(self.rect().left() + frame_width + 5,
                                (self.rect().bottom() - clear_button_size.height() + 1)/2)
        self.clear_button.move(self.rect().right() - frame_width - clear_button_size.width() - 5,
                               (self.rect().bottom() - clear_button_size.height() + 1)/2)
        super(SearchLineEdit, self).resizeEvent(event)

    def set_completer(self, complete_list):
        """
        :param complete_list: <list>
        :return:
        """
        completer = QCompleter(complete_list, self)
        style = "QListView{color: #fff; border: 0px;outline: none;border-style: solid;" \
                "margin: 0px 0px 0px 0px;padding: 0px 0px 0px 0px;background-color: #2d2f37}"
        completer.popup().setStyleSheet(style)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.setCompleter(completer)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = SearchLineEdit()
    win.show()
    win.set_completer(["aha", "bcad", "cfj"])
    sys.exit(app.exec_())
