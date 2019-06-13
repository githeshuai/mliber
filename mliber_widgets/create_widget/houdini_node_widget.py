# -*- coding:utf-8 -*-
from create_widget import CreateWidget


class HoudiniNodeWidget(CreateWidget):
    library_type = "HoudiniNode"

    def __init__(self, parent=None):
        super(HoudiniNodeWidget, self).__init__(self.library_type, parent)
