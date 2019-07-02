# -*- coding:utf-8 -*-
from Qt.QtWidgets import QDialog, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QCheckBox, QPushButton
import mliber_resource


class UnrealImportOptionsWidget(QDialog):
    def __init__(self, parent=None):
        super(UnrealImportOptionsWidget, self).__init__(parent)
        self.as_skeletal = None
        self.materials = None
        self.textures = None
        self.setWindowTitle("Import Options")
        self.resize(300, 100)
        main_layout = QVBoxLayout(self)
        # grid layout
        options_layout = QGridLayout()
        skeletal_label = QLabel("Skeletal Mesh", self)
        self.skeletal_check = QCheckBox(self)
        material_label = QLabel("Import Materials", self)
        self.material_check = QCheckBox(self)
        texture_label = QLabel("Import Textures", self)
        self.texture_check = QCheckBox(self)
        options_layout.addWidget(skeletal_label, 0, 0, 1, 1)
        options_layout.addWidget(self.skeletal_check, 0, 1, 1, 1)
        options_layout.addWidget(material_label, 1, 0, 1, 1)
        options_layout.addWidget(self.material_check, 1, 1, 1, 1)
        options_layout.addWidget(texture_label, 2, 0, 1, 1)
        options_layout.addWidget(self.texture_check, 2, 1, 1, 1)
        # button layout
        button_layout = QHBoxLayout()
        self.import_btn = QPushButton("Import", self)
        self.cancel_btn = QPushButton("Cancel", self)
        button_layout.addStretch()
        button_layout.addWidget(self.import_btn)
        button_layout.addWidget(self.cancel_btn)
        # add to main layout
        main_layout.addLayout(options_layout)
        main_layout.addLayout(button_layout)
        main_layout.setSpacing(15)
        # set signals
        self._set_signals()
        self._set_style()

    def _set_signals(self):
        """
        set signals
        :return:
        """
        self.import_btn.clicked.connect(self._on_import_btn_clicked)
        self.cancel_btn.clicked.connect(self._on_cancel_btn_clicked)
        self.accepted.connect(self._set_attr)

    def _set_style(self):
        """
        set stylesheet
        :return:
        """
        self.setStyleSheet(mliber_resource.style())

    def _import_materials(self):
        """
        是否导入材质
        :return: <bool>
        """
        return self.material_check.isChecked()

    def _import_textures(self):
        """
        是否导入贴图
        :return: <bool>
        """
        return self.texture_check.isChecked()

    def _import_as_skeleton(self):
        """
        是否导入骨架
        :return: <bool>
        """
        return self.skeletal_check.isChecked()

    def _on_import_btn_clicked(self):
        """
        :return:
        """
        self.accept()

    def _on_cancel_btn_clicked(self):
        """
        :return:
        """
        self.reject()

    def _set_attr(self):
        """
        set material and texture attribute
        :return:
        """
        self.as_skeletal = self._import_as_skeleton()
        self.materials = self._import_materials()
        self.textures = self._import_textures()


if __name__ == "__main__":
    from Qt.QtWidgets import QApplication
    app = QApplication([])
    a = UnrealImportOptionsWidget()
    a.show()
    app.exec_()
    print a.as_skeletal, a.materials, a.textures

