#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date      : 2019-12-16 11:32
# Author    : Mr.He
# Usage     : 
# Version   :
# Comment   :


# Import built-in modules

# Import third-party modules
from Qt.QtWidgets import *
from Qt.QtCore import *
# Import local modules
import mliber_global
from mliber_settings import Settings

SETTINGS = Settings(mliber_global.user().name)


class DescriptionWidget(QWidget):
    def __init__(self, parent=None):
        super(DescriptionWidget, self).__init__(parent)
        self._setup_ui()
        self._set_signals()
        self._init()

    def _set_color(self, color):
        """
        set color
        :param color: <list> [r, g, b]
        :return:
        """
        self._color = color
        self.color_checker.setStyleSheet("background: rgba(%s)" % ",".join(self._color))

    def _setup_ui(self):
        """
        setup ui
        :return:
        """
        main_layout = QFormLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.color_checker = QPushButton("Click to select color", self)
        self.size_combo = QComboBox(self)
        self.size_combo.addItems(["6", "8", "10", "12", "14", "16", "18", "20"])
        main_layout.addRow("Color", self.color_checker)
        main_layout.addRow("Size", self.size_combo)

    def _init(self):
        """init"""
        color = [str(i) for i in SETTINGS.paint_color()]
        self._set_color(color)
        # size
        size = SETTINGS.paint_size()
        self.size_combo.setCurrentIndex(self.size_combo.findText(str(size)))

    def _set_signals(self):
        """
        set signals
        :return:
        """
        self.color_checker.clicked.connect(self._select_color)

    def _select_color(self):
        """
        select color
        :return:
        """
        color_dialog = QColorDialog(self)
        color_dialog.currentColorChanged.connect(self._on_color_changed)
        color_dialog.show()

    def _on_color_changed(self, color):
        """
        :param color:
        :return:
        """
        color = [str(i) for i in color.toTuple()]
        self._set_color(color)

    def color(self):
        """
        :return: <list>
        """
        return [int(i) for i in self._color]

    def size(self):
        """
        get size
        :return:
        """
        return int(self.size_combo.currentText())


class SettingsDialog(QDialog):
    setting_finished_signal = Signal()

    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setWindowTitle("Settings")
        self.resize(400, 200)
        self._setup_ui()
        self._set_signals()
        self._init()

    def _setup_ui(self):
        """
        setup ui
        :return:
        """
        main_layout = QVBoxLayout(self)
        # form layout
        form_layout = QFormLayout()
        self.max_icon_size_combo = QComboBox(self)
        self.max_icon_size_combo.addItems(["256", "512", "1024", "2048"])
        self.paint_description_check = QCheckBox(self)
        self.description_widget = DescriptionWidget(self)
        self.show_flag_check = QCheckBox(self)
        self.show_asset_name_check = QCheckBox(self)
        # button layout
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        # add to form layout
        form_layout.addRow("Max Icon Size", self.max_icon_size_combo)
        form_layout.addRow("Paint Description", self.paint_description_check)
        form_layout.addWidget(self.description_widget)
        form_layout.addRow("Show Asset Flag", self.show_flag_check)
        form_layout.addRow("Show Asset Name", self.show_asset_name_check)
        # add to main layout
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

    def _set_signals(self):
        """
        set signals
        :return:
        """
        self.paint_description_check.stateChanged.connect(self._show_or_hide_description_widget)
        self.cancel_btn.clicked.connect(self.close)
        self.save_btn.clicked.connect(self._save_settings)

    def _init(self):
        """
        init
        :return:
        """
        max_icon_size = SETTINGS.max_icon_size()
        self.max_icon_size_combo.setCurrentIndex(self.max_icon_size_combo.findText(str(max_icon_size)))
        self.paint_description_check.setChecked(SETTINGS.paint_description())
        self._show_or_hide_description_widget()
        self.show_flag_check.setChecked(SETTINGS.show_asset_flag())
        self.show_asset_name_check.setChecked(SETTINGS.show_asset_name())

    def _show_or_hide_description_widget(self):
        """
        显示或者隐藏description widget
        :return:
        """
        self.description_widget.setHidden(not self.paint_description_check.isChecked())

    def _save_settings(self):
        """
        save settings
        :return:
        """
        max_icon_size = int(self.max_icon_size_combo.currentText())
        paint_description = self.paint_description_check.isChecked()
        paint_color = self.description_widget.color()
        paint_size = self.description_widget.size()
        show_asset_flag = self.show_flag_check.isChecked()
        show_asset_name = self.show_asset_name_check.isChecked()
        data = dict(max_icon_size=max_icon_size, paint_description=paint_description,
                    paint_color=paint_color, paint_size=paint_size,
                    show_asset_flag=show_asset_flag, show_asset_name=show_asset_name)
        SETTINGS.update(data)
        SETTINGS.write_out()
        self.setting_finished_signal.emit()
        self.close()


if __name__ == "__main__":
    app = QApplication.instance()
    if not app:
        app = QApplication(["settings"])
    sd = SettingsDialog()
    sd.show()
    sys.exit(app.exec_())
