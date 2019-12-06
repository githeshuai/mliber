#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date      : 2019-12-03 16:31
# Author    : Mr. He
# Version   :
# Usage     : 
# Notes     :

# Import built-in modules

# Import third-party modules
from Qt.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QButtonGroup, QCheckBox
from Qt.QtCore import Qt
# Import local modules
from mliber_parse.library_parser import Library
from mliber_parse.element_type_parser import ElementType


class ActionWidget(QWidget):
    """
    根据配置信息显示check box
    """
    def __init__(self, library_type, engine=None, parent=None):
        super(ActionWidget, self).__init__(parent)
        self._library_type = library_type
        self._engine = engine
        # self settings
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # actions label
        action_label = QLabel(self)
        action_label.setText("<font color=#fff size=4><b>Actions</b></font>")
        main_layout.addWidget(action_label)
        # scroll area
        scroll_area = QScrollArea(self)
        scroll_area.setMinimumHeight(150)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFocusPolicy(Qt.NoFocus)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # set widget
        widget = QWidget(self)
        self.scroll_layout = QVBoxLayout(widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_layout.setContentsMargins(20, 0, 0, 0)
        self.scroll_layout.setSpacing(5)
        scroll_area.setWidget(widget)
        # add checkboxes
        self.action_btngrp = QButtonGroup()
        self.action_btngrp.setExclusive(False)
        check_box_list = self.create_checkboxes()
        for check_box in check_box_list:
            self.action_btngrp.addButton(check_box)
            self.scroll_layout.addWidget(check_box)
        main_layout.addWidget(scroll_area)

    def types(self):
        """
        get all actions from configuration file
        Returns:
        """
        return Library(self._library_type).types()

    def create_checkboxes(self):
        """
        create actions
        Returns:list of QCheckBox
        """
        checkbox_list = list()
        types = self.types()
        if types:
            for typ in types:
                action_object = ElementType(typ).export_action_of_engine(self._engine)
                if not action_object:
                    continue
                name = action_object.name
                checked = action_object.default
                check_box = QCheckBox(name, self)
                check_box.setChecked(checked)
                check_box.type = action_object.type  # element type
                checkbox_list.append(check_box)
        return checkbox_list

    def checked_buttons(self):
        """
        获取
        :return:
        """
        return [button for button in self.action_btngrp.buttons() if button.isChecked()]


