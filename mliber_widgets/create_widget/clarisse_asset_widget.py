# -*- coding: utf-8 -*-
from create_widget import CreateWidget


class ClarisseAssetWidget(CreateWidget):
    library_type = "ClarisseAsset"

    def __init__(self, parent=None):
        super(ClarisseAssetWidget, self).__init__(self.library_type, parent)
