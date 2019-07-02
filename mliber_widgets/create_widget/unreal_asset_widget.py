# -*- coding:utf-8 -*-
from create_widget import CreateWidget


class UnrealAssetWidget(CreateWidget):
    library_type = "UnrealAsset"

    def __init__(self, parent=None):
        super(UnrealAssetWidget, self).__init__(self.library_type, parent)
