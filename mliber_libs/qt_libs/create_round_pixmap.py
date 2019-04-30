# -*- coding: utf-8 -*-
from Qt.QtGui import QPixmap, QImage, QBrush, QPainter
from Qt.QtCore import Qt


def create_round_pixmap(image_path, scale_size):
    """
    Create a custom px wide circle thumbnail
    :param image_path: a png file path
    :param scale_size: scale size of the image
    :return: QPixmap
    """
    # get the 512 base image
    base_image = QPixmap(scale_size, scale_size)
    base_image.fill(Qt.transparent)
    # now attempt to load the image
    image = QImage(image_path)
    thumb = QPixmap.fromImage(image)
    # pixmap will be a null pixmap if load fails
    if not thumb.isNull():
        # scale it down to fit inside a frame of maximum 512x512
        thumb_scaled = thumb.scaled(scale_size,
                                    scale_size,
                                    # Qt.KeepAspectRatioByExpanding,
                                    Qt.IgnoreAspectRatio,
                                    Qt.SmoothTransformation)

        # now composite the thumbnail on top of the base image
        # bottom align it to make it look nice
        thumb_img = thumb_scaled.toImage()
        brush = QBrush(thumb_img)
        painter = QPainter(base_image)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, scale_size, scale_size)
        painter.end()

    return base_image
