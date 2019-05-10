# -*- coding:utf-8 -*-
from Qt.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QTextEdit, QPushButton
from Qt.QtCore import Signal, Qt
from mliber_qt_components.path_widget import PathWidget
from mliber_qt_components.choose_path_widget import ChoosePathWidget
from mliber_qt_components.messagebox import MessageBox
from mliber_conf.library_type import LIBRARY_TYPE


class CreateLibraryDialog(QDialog):
    create = Signal(list)
    update = Signal(list)

    def __init__(self, mode="create", parent=None):
        """
        built in init
        :param mode: <str> create or update
        :param parent:
        """
        super(CreateLibraryDialog, self).__init__(parent)
        self.mode = mode
        self.setWindowTitle("Create Library")
        self.resize(400, 350)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(4, 4, 4, 4)
        # name layout
        name_layout = QHBoxLayout()
        name_label = QLabel(self)
        name_label.setText("<font color=#f00>*</font>name")
        name_label.setAlignment(Qt.AlignRight)
        self.name_le = QLineEdit(self)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_le)
        # type layout
        type_layout = QHBoxLayout()
        type_label = QLabel(self)
        type_label.setFixedWidth(35)
        type_label.setAlignment(Qt.AlignRight)
        type_label.setText("<font color=#f00>*</font>type")
        self.type_combo = QComboBox(self)
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)
        # path widget
        self.path_widget = PathWidget(self)
        self.choose_path_widget = ChoosePathWidget(self)
        self.choose_path_widget.set_label_text(u"图标")
        # description
        description_layout = QHBoxLayout()
        description_label = QLabel(u"描述", self)
        description_label.setMinimumWidth(31)
        description_label.setAlignment(Qt.AlignTop)
        self.description_te = QTextEdit(self)
        description_layout.addWidget(description_label)
        description_layout.addWidget(self.description_te)
        # button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.exec_button = QPushButton(self)
        if self.mode == "create":
            self.exec_button.setText("Create")
        else:
            self.exec_button.setText("Update")
        button_layout.addWidget(self.exec_button)
        self.close_btn = QPushButton("Close", self)
        button_layout.addWidget(self.close_btn)
        # add to main layout
        main_layout.addLayout(name_layout)
        main_layout.addLayout(type_layout)
        main_layout.addWidget(self.path_widget)
        main_layout.addWidget(self.choose_path_widget)
        main_layout.addLayout(description_layout)
        main_layout.addLayout(button_layout)
        # init
        self.init()
        # set signals
        self.set_signals()

    def init(self):
        """
        initialize
        :return:
        """
        self.type_combo.addItems(LIBRARY_TYPE)

    def set_signals(self):
        """
        :return:
        """
        self.exec_button.clicked.connect(self.on_exec_btn_clicked)
        self.close_btn.clicked.connect(self.close)

    @property
    def name(self):
        """
        :return:<str>
        """
        return self.name_le.text()

    def set_name(self, name):
        """
        set name
        :param name: <str>
        :return:
        """
        self.name_le.setText(name)

    @property
    def type(self):
        """
        :return: <str>
        """
        return self.type_combo.currentText()

    def set_type(self, typ):
        """
        set type
        :param typ: <str>
        :return:
        """
        self.type_combo.setCurrentIndex(self.type_combo.findText(typ))

    @property
    def windows_path(self):
        """
        windows path
        :return:
        """
        return self.path_widget.windows_path().replace("\\", "/")

    def set_windows_path(self, path):
        """
        set windows path
        :param path:
        :return:
        """
        path = path if path else ""
        self.path_widget.set_windows_path(path)

    @property
    def linux_path(self):
        """
        linux path
        :return:
        """
        return self.path_widget.linux_path().replace("\\", "/")

    def set_linux_path(self, path):
        """
        set linux path
        :param path:
        :return:
        """
        path = path if path else ""
        self.path_widget.set_linux_path(path)

    @property
    def mac_path(self):
        """
        mac path
        :return:
        """
        return self.path_widget.mac_path().replace("\\", "/")

    def set_mac_path(self, path):
        """
        set mac path
        :param path: <str>
        :return:
        """
        path = path if path else ""
        self.path_widget.set_mac_path(path)

    @property
    def icon_path(self):
        """
        mac path
        :return:
        """
        return self.choose_path_widget.path.replace("\\", "/")

    def set_icon_path(self, path):
        """
        set icon path
        :param path: <str> a png file path
        :return:
        """
        self.choose_path_widget.set_path(path)

    @property
    def description(self):
        """
        :return: <str>
        """
        return self.description_te.toPlainText()

    def set_description(self, description):
        """
        set description
        :return:
        """
        self.description_te.setText(description)

    def on_exec_btn_clicked(self):
        """
        当create button click
        :return:
        """
        if not all((self.name, self.type)):
            MessageBox.warning(self, "Warning", u"请填入必填项")
            return
        data = [self.name, self.type, self.windows_path, self.linux_path,
                self.mac_path, self.icon_path, self.description]
        if self.mode == "create":
            self.create.emit(data)
        else:
            self.update.emit(data)
