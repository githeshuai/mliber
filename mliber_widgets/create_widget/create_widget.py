# -*- coding:utf-8 -*-
from Qt.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QButtonGroup, QCheckBox
from Qt.QtCore import Qt


class TitleLabel(QLabel):
    def __init__(self, text, must=False, parent=None):
        super(TitleLabel, self).__init__(parent)
        self.setAlignment(Qt.AlignRight)
        self.name = text
        if must:
            self.set_must()
        else:
            self.setText(self.name)
        self.setMinimumWidth(53)
        self.setStyleSheet("color: #777777")

    def set_must(self):
        """
        设置为必填
        Returns:
        """
        text = self.name
        new_text = "<font color=#f00>*</font>%s" % text
        self.setText(new_text)


class ActionScrollArea(QScrollArea):
    """
    根据配置信息显示check box
    """
    def __init__(self, library, parent=None):
        super(ActionScrollArea, self).__init__(parent)
        self.library = library
        # self settings
        self.setMinimumHeight(150)
        self.setWidgetResizable(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # set widget
        widget = QWidget(self)
        self.scroll_layout = QVBoxLayout(widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_layout.setContentsMargins(20, 0, 0, 0)
        self.scroll_layout.setSpacing(5)
        self.setWidget(widget)
        # action label
        action_label = QLabel("Actions")
        self.scroll_layout.addWidget(action_label)
        # add checkboxes
        self.action_btngrp = QButtonGroup()
        self.action_btngrp.setExclusive(False)
        check_box_list = self.create_checkboxes()
        for check_box in check_box_list:
            self.action_btngrp.addButton(check_box)
            self.scroll_layout.addWidget(check_box)

    def action_objects(self):
        """
        get all actions from configuration file
        Returns:
        """
        return Library(self.library).actions

    def create_checkboxes(self):
        """
        create actions
        Returns:list of QCheckBox
        """
        checkbox_list = list()
        action_objects = self.action_objects()
        if action_objects:
            for action_object in action_objects:
                name = action_object.name
                api_arg = action_object.api_arg
                checked = action_object.checked
                check_box = QCheckBox(name, self)
                check_box.setChecked(checked)
                check_box.api_arg = api_arg
                checkbox_list.append(check_box)
        return checkbox_list


class CreateWidget(QWidget):
    def __init__(self, parent=None):
        super(CreateWidget, self).__init__(parent)
        main_layout = QVBoxLayout(self)


