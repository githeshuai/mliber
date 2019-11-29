# -*- coding:utf-8 -*-
from Qt.QtWidgets import QPushButton, QWidgetAction, QLabel, QMenu, QToolButton, QAction
from Qt.QtCore import Qt, Slot, QSize, QRect, QPoint
from mliber_conf import mliber_config
import mliber_resource


class ShelfButtonAction(QWidgetAction):
    def __init__(self, text, parent=None):
        """
        built in
        :param text: <str> action text
        :param parent:
        """
        super(ShelfButtonAction, self).__init__(parent)
        self._text = QLabel(text, parent)
        self._text.setMinimumHeight(25)
        self._text.setStyleSheet("font: bold;font-family: Arial;font-size: 14px;")
        self.setDefaultWidget(self._text)


class ShelfButtonMenu(QMenu):
    def __init__(self, parent=None):
        super(ShelfButtonMenu, self).__init__(parent)
        self.setMouseTracking(True)
        self._parent = parent
        self._parent_rect = None
        self.resize_parent_rect()
        self.aboutToShow.connect(self._set_minimum_width)

    @Slot()
    def _set_minimum_width(self):
        """
        set minimum width
        :return:
        """
        self.setMinimumWidth(self.parent().width())

    def mouseMoveEvent(self, event):
        super(ShelfButtonMenu, self).mouseMoveEvent(event)
        if not self.rect().contains(event.pos()) and not self._parent_rect.contains(event.pos()):
            self.hide()
            self._parent.set_default_style()

    def resize_parent_rect(self):
        self._parent_rect = QRect(QPoint(0, -1*self.parent().height()), self.parent().size())


class ShelfButton(QToolButton):
    def __init__(self, text, parent=None):
        """
        built in
        :param text: <str> button text
        :param parent:
        """
        super(ShelfButton, self).__init__(parent)
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.setFocusPolicy(Qt.NoFocus)
        self.setText(text)
        self.setMinimumSize(60, 30)
        self._default_style = "QToolButton{background: transparent; font-size: 13px; font: bold; color: #FFF;" \
                              "Text-align:left; padding-left: 5px;}" \
                              "QToolButton::menu-indicator {image: none;}"
        self._hover_style = self._default_style + ("QToolButton:hover{color: %s;background: %s;}" %
                                                   (mliber_config.ACCENT_COLOR, mliber_config.MENU_COLOR))
        self.set_hover_style()
        self.triggered.connect(self.set_default_style)

    def set_default_style(self):
        """
        set default style
        :return:
        """
        self.setStyleSheet(self._default_style)

    def set_hover_style(self):
        """
        set hover style
        :return:
        """
        self.setStyleSheet(self._hover_style)

    def enterEvent(self, event):
        super(ShelfButton, self).enterEvent(event)
        if self.menu() and self.menu().isHidden():
            self.set_hover_style()
            self.showMenu()

    def resizeEvent(self, event):
        super(ShelfButton, self).resizeEvent(event)
        if self.menu():
            self.menu().resize_parent_rect()

    def set_tip(self, text=None):
        if not text:
            self.setToolTip(self.__class__.__name__)
        else:
            self.setToolTip(text)

    def set_menu(self, menu=None):
        """
        set menu
        :param menu: <ShelfButtonMenu>
        :return:
        """
        if not menu:
            menu = ShelfButtonMenu(self)
        self.setMenu(menu)

    def add_menu_action(self, text, command, checkable=False, checked=False, short_cut="", icon_name=""):
        """
        add menu action
        :param text: <str>
        :param command: <func> when triggered action run the command
        :param checkable: <bool> whether this action is check able
        :param checked: <bool> whether this action is checeked
        :param short_cut: <str> set this action shortcut
        :param icon_name: <str> an icon path
        :return:
        """
        if self.menu():
            act = QAction(text, self.menu(), triggered=command)
            act.setCheckable(checkable)
            if checkable:
                act.setChecked(checked)
            if short_cut:
                self.setShortcut(short_cut)
            if icon_name:
                act.setIcon(mliber_resource.icon(icon_name))
            self.menu().addAction(act)

    def add_menu_separator(self):
        """
        add menu separator
        :return:
        """
        if self.menu():
            self.menu().addSeparator()

    def set_icon(self, icon_name):
        """
        :param icon_name: <str>
        :return:
        """
        self.setIcon(mliber_resource.icon(icon_name))


class IndicatorButton(QPushButton):
    def __init__(self, text, parent=None):
        super(IndicatorButton, self).__init__(text, parent)
        self.setFocusPolicy(Qt.NoFocus)
        self.setStyleSheet("QPushButton{background: transparent; font-size: 13px; font: bold; color: #FFF; "
                           "Text-align:left; width: 60px; padding-left: 5px;}"
                           "QPushButton::hover{color: %s;}" % mliber_config.ACCENT_COLOR)
