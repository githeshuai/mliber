# -*- coding:utf-8 -*-
from functools import partial
from Qt.QtWidgets import QStyledItemDelegate, QStyle
from Qt.QtGui import QColor, QIcon, QPixmap, QPainter, QFont, QPen, QBrush
from Qt.QtCore import QSize, Qt, QModelIndex, QRect
import mliber_global
import mliber_resource
from mliber_conf import mliber_config


FONT_HEIGHT = 18
DEFAULT_COLOR = QColor(138, 138, 138)


class AssetDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(AssetDelegate, self).__init__(parent)
        self._parent = parent
        self._model = self._parent.model()
        self._source_model = self._model.sourceModel()
        self._margin = 1
        self._image_server = mliber_global.image_server()
        self._image_server.cache_done_signal.connect(self._img_cached_done)
        self._default_img = mliber_resource.pixmap("image.png")
        self._sequence_img = mliber_resource.pixmap("video.png")

    def _img_cached_done(self, *args):
        """
        当图片缓存成功，刷新ui
        :param args:
        :return:
        """
        self._parent.setUpdatesEnabled(False)
        self._parent.repaint()
        self._parent.setUpdatesEnabled(True)

    def sizeHint(self, option, index):
        item = self._parent.item_at_index(index)
        size = QSize(item.icon_size.width(), item.icon_size.height())
        return size

    def paint(self, painter, option, index):
        painter.save()
        try:
            painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
            self.paintBackground(painter, option, index)
            item = self._parent.item_at_index(index)
            if option.state & QStyle.State_MouseOver:
                if item.has_sequence and not item.started:
                    item.start()
            else:
                if item.started:
                    item.pause()
            if item.has_sequence:
                img_item = QPixmap(item.current_filename)
                self._draw_progress(painter, option, item)
            else:
                img_item = self._image_server.get_image(item.current_filename)
            image = img_item or self._default_img
            rect = self._draw_centralized_pic(painter, option, image)
            self._draw_text(painter, option, item.name)
        finally:
            painter.restore()

    def paintBackground(self, painter, option, index):
        """
        Draw the background for the item.

        :type painter: QtWidgets.QPainter
        :type option: QtWidgets.QStyleOptionViewItem
        :type index: QtCore.QModelIndex
        :rtype: None
        """
        is_selected = option.state & QStyle.State_Selected
        is_mouse_over = option.state & QStyle.State_MouseOver
        painter.setPen(QPen(Qt.NoPen))
        if is_selected:
            color = QColor(57, 255, 255)
            painter.setBrush(QBrush(color))
        elif is_mouse_over:
            color = mliber_config.ICON_HOVER_COLOR
            painter.setBrush(QBrush(color))
        else:
            color = QColor(57, 60, 70)
            painter.setBrush(QBrush(color))
        painter.drawRect(option.rect)

    def _draw_centralized_pic(self, painter, option, img):
        """
        画图
        :param painter:
        :param rect:
        :param img:
        :return:
        """
        rect_margin = [0, 0, 0, -20]
        img_rect = option.rect.adjusted(
            self._margin + rect_margin[0], self._margin + rect_margin[1],
            -self._margin + rect_margin[2], -self._margin + rect_margin[3])
        img_rect_width, img_rect_height = float(img_rect.width()), float(img_rect.height())
        cur_img = img
        cur_img_width, cur_img_height = float(cur_img.width()), float(cur_img.height())
        cur_img_w_h_ratio = cur_img_width / cur_img_height
        if cur_img_w_h_ratio > 1:
            scale_ratio = img_rect_width / cur_img_width
        else:
            scale_ratio = img_rect_height / cur_img_height
        img_adjusted_rect = QRect(
            img_rect.x() + (img_rect_width - cur_img_width * scale_ratio) / 2,
            img_rect.y() + (img_rect_height - cur_img_height * scale_ratio) / 2,
            cur_img_width * scale_ratio, cur_img_height * scale_ratio
        )
        if type(img) == QPixmap:
            painter.drawPixmap(img_adjusted_rect, img)
        else:
            painter.drawImage(img_adjusted_rect, img)
        self._img_cached_done()
        return img

    @staticmethod
    def _draw_text(painter, option, text):
        """
        painter 文字
        :param painter:
        :param option:
        :param text:
        :return:
        """
        rect = option.rect
        font = QFont("Arial", 8, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))
        if option.state & QStyle.State_Selected:
            painter.setPen(QColor(0, 0, 0))
        if option.state & QStyle.State_MouseOver:
            painter.setPen(QColor(0, 0, 0))
        text_rect = QRect(rect.adjusted(0, 0, 0, -20).bottomLeft(), rect.bottomRight())
        painter.drawText(text_rect, Qt.AlignCenter, text)

    def _draw_progress(self, painter, option, item):
        """
        画进度条
        :param painter:
        :param option:
        :param item:
        :return:
        """
        if item.current_filename:
            r = option.rect
            brush_color = QColor(57, 255, 255)
            image_sequence = item.image_sequence
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(brush_color))
            if image_sequence.percent() <= 0:
                width = 0
            elif image_sequence.percent() >= 1:
                width = r.width()
            else:
                width = image_sequence.percent() * r.width() + 1
            height = 2
            y = r.y() + r.height() - (height - 1)
            painter.drawRect(r.x(), y, width, height)
