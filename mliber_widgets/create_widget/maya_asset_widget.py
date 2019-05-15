# -*- coding:utf-8 -*-
from create_widget import CreateWidget
from mliber_qt_components.input_text_edit import InputTextEdit
from mliber_qt_components.messagebox import MessageBox


class MayaAssetWidget(CreateWidget):
    library_type = "MayaAsset"

    def __init__(self, parent=None):
        super(MayaAssetWidget, self).__init__(self.library_type, parent)
        self.show_thumbnail()
        self.show_actions()
        self.show_frame_range()

    def preflight(self):
        """
        重写基类的preflight
        :return:
        """
        if not self.thumbnail:
            MessageBox.warning(self, "Warning", u"没有缩略图")
            return False
        return True

    def run(self):
        pass



if __name__ == "__main__":
    from mliber_libs.qt_libs.render_ui import render_ui
    with render_ui():
        s = MayaAssetWidget()
        s.show()
