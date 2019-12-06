# -*- coding:utf-8 -*-
from mliber_widgets.create_widget.create_widget import CreateWidget


class NukeNodeWidget(CreateWidget):
    library_type = "NukeNode"

    def __init__(self, parent=None):
        super(NukeNodeWidget, self).__init__(self.library_type, parent)
