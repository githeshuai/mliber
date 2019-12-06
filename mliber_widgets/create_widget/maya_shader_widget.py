# -*- coding:utf-8 -*-
from mliber_widgets.create_widget.create_widget import CreateWidget


class MayaShaderWidget(CreateWidget):
    library_type = "MayaShader"

    def __init__(self, parent=None):
        super(MayaShaderWidget, self).__init__(self.library_type, parent)

