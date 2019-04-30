# -*- coding: utf-8 -*-
from Qt.QtCore import QSize, Qt


def resize_pixmap_to_label(pixmap, label):
    """
    :param pixmap: QPixmap
    :param label: QLabel
    :return:
    """
    label_width = label.width()
    label_height = label.height()
    image_width = pixmap.width()
    image_height = pixmap.height()
    if image_width > image_height:
        scaled = pixmap.scaled(QSize(label_width, image_width / label_width * image_height),
                               Qt.KeepAspectRatio, Qt.SmoothTransformation)
    elif image_width < image_height:
        scaled = pixmap.scaled(QSize(image_height / label_height * image_width, label_height),
                               Qt.KeepAspectRatio, Qt.SmoothTransformation)
    else:
        scaled = pixmap.scaled(QSize(label_width, label_height),
                               Qt.KeepAspectRatio, Qt.SmoothTransformation)
    return scaled
