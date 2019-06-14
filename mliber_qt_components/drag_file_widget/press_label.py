# -*- coding: utf-8 -*-
from Qt.QtWidgets import QLabel, QFileDialog
from Qt.QtCore import Signal, Qt


class PressLabel(QLabel):
    clicked = Signal(list)

    def __init__(self, parent=None):
        super(PressLabel, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setWordWrap(True)
        self.setText("Drag and drop files here or clicked to browse")
        self.set_style()

    def set_style(self):
        self.setStyleSheet("QLabel{padding: 3px;border: 2px dashed #666666;border-radius:0px;"
                           "font: bold 12px/50px Arial, sans-serif;color:#666666;"
                           "qproperty-alignment: 'AlignCenter';}"
                           "QLabel:hover{border-color:#2194c4;color:#2194c4}")

    def mousePressEvent(self, event):
        super(PressLabel, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            files, ok = QFileDialog.getOpenFileNames(self, "Choose files")
            if ok:
                self.clicked.emit(files)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        paths = list()
        for url in event.mimeData().urls():
            try:
                path = str(url.toLocalFile())
            except Exception as e:
                print str(e)
            paths.append(path)
        self.clicked.emit(paths)
