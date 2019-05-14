# -*- coding:utf-8 -*-
from Qt.QtWidgets import QToolButton, QStyle
from Qt.QtGui import QColor, QIcon
from Qt.QtCore import QSize, Qt, Signal
from mliber_qt_components.icon import Icon
import mliber_resource


class ToolButton(QToolButton):
    def __init__(self, parent=None):
        super(ToolButton, self).__init__(parent)
        self.default_icon_color = QColor(180, 180, 180)
        self.setMouseTracking(True)
        self.setStyleSheet("QToolButton{border: 0px; padding: 0px; background:transparent} "
                           "QToolButton::hover{background:transparent}")

    def set_icon(self, icon_path):
        icon = Icon(icon_path)
        icon.set_color(self.default_icon_color)
        self.setIcon(icon)

    def enterEvent(self, event):
        icon = Icon(self.icon())
        icon.set_color(QColor(255, 0, 0))
        self.setIcon(icon)

    def leaveEvent(self, event):
        icon = Icon(self.icon())
        icon.set_color(self.default_icon_color)
        self.setIcon(icon)


class IconButton(QToolButton):
    delete_signal = Signal()

    def __init__(self, parent=None):
        super(IconButton, self).__init__(parent)
        self._height = 20
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.clear_button = self.create_clear_button()
        self.clear_button.clicked.connect(self._delete)
        self.setStyleSheet('border: 0px solid; padding: 0px; background: #2d2f37;')

    def set_height(self, height):
        """
        set icon size
        :param height: <int>
        :return:
        """
        self._height = height
        self.setFixedHeight(height)
        self.setIconSize(QSize(height*0.8, height*0.8))
        self.clear_button.setFixedSize(QSize(height, height))
        self.clear_button.setIconSize(QSize(height*0.5, height*0.5))

    def set_icon(self, icon_path):
        """
        :param icon_path: <str>
        :return:
        """
        icon = QIcon(icon_path)
        self.setIcon(icon)

    def set_icon_color(self, color):
        """
        :param color: QColor
        :return:
        """
        icon = Icon(self.icon())
        icon.set_color(color)
        self.setIcon(icon)

    def create_clear_button(self):
        """
        create clear button
        Returns:
        """
        clear_button = ToolButton(self)
        clear_button.set_icon(mliber_resource.icon_path("remove.png"))
        clear_button.setStyleSheet('border: 0px; padding: 0px; background: transparent;')
        clear_button.setCursor(Qt.ArrowCursor)
        clear_button.setVisible(False)
        return clear_button

    def _delete(self):
        """
        delete self
        :return:
        """
        self.deleteLater()
        self.delete_signal.emit()

    def resizeEvent(self, event):
        clear_button_size = self.clear_button.sizeHint()
        frame_width = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        self.clear_button.move(self.rect().right() - frame_width - clear_button_size.width() - 10,
                               self.rect().bottom() - self.height())
        super(IconButton, self).resizeEvent(event)

    def enterEvent(self, event):
        self.clear_button.setVisible(True)

    def leaveEvent(self, event):
        self.clear_button.setVisible(False)


if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        i = IconButton()
        i.set_icon(r"E:\mliber\mliber_icons\refresh.png")
        i.set_height(60)
        i.show()
