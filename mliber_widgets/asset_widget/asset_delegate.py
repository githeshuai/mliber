# -*- coding:utf-8 -*-
from Qt.QtWidgets import QStyledItemDelegate, QStyle
from Qt.QtGui import QColor, QIcon, QPixmap, QPainter, QFont, QPen, QBrush
from Qt.QtCore import QSize, Qt, QModelIndex, QRect
import mliber_global
import mliber_resource
from mliber_conf import mliber_config
from mliber_custom import PAINT_DESCRIPTION, DESCRIPTION_COLOR, DESCRIPTION_FONT_SIZE


PADDING = 2
FLAG_SIZE = 14


class AssetDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(AssetDelegate, self).__init__(parent)
        self._parent = parent
        self._model = self._parent.model()
        self._source_model = self._model.sourceModel()
        self._margin = 1
        self._image_server = mliber_global.image_server()
        self._image_server.cache_done_signal.connect(self._img_cached_done)
        # image
        self._default_img = mliber_resource.pixmap("image.png")
        self._sequence_img = mliber_resource.pixmap("video.png")
        self._store_img = mliber_resource.pixmap("store.png")
        self._no_store_img = mliber_resource.pixmap("no_store.png")
        self._description_img = mliber_resource.pixmap("description.png")
        self._no_description_img = mliber_resource.pixmap("no_description.png")
        self._tag_img = mliber_resource.pixmap("tag.png")
        self._no_tag_img = mliber_resource.pixmap("no_tag.png")

    def _store_image_of_item(self, item):
        """
        获取store image
        :param item:
        :return:
        """
        if item.stored_by_me:
            return self._store_img
        return self._no_store_img

    def _description_image_of_item(self, item):
        """
        获取description image
        :param item:
        :return:
        """
        if item.description:
            return self._description_img
        return self._no_description_img

    def _tag_image_of_item(self, item):
        """
        获取description image
        :param item:
        :return:
        """
        if item.has_tag:
            return self._tag_img
        return self._no_tag_img

    def _img_cached_done(self, *args):
        """
        当图片缓存成功，刷新ui
        :param args:
        :return:
        """
        self._parent.refresh_self()

    def sizeHint(self, option, index):
        item = self._parent.item_at_index(index)
        if self._parent.show_asset_flag and self._parent.show_asset_name:
            size = QSize(item.icon_size.width(), item.icon_size.height() + 40)
        else:
            if (not self._parent.show_asset_flag) and (not self._parent.show_asset_name):
                size = QSize(item.icon_size.width(), item.icon_size.height())
            else:
                size = QSize(item.icon_size.width(), item.icon_size.height() + 20)
        return size

    def paint(self, painter, option, index):
        painter.save()
        try:
            painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
            self.draw_background(painter, option)
            item = self._parent.item_at_index(index)
            if option.state & QStyle.State_MouseOver:
                if item.has_sequence and not item.started:
                    item.start()
            else:
                if item.started:
                    item.pause()
            if item.has_sequence:
                q_image = QPixmap(item.current_filename)
                self._draw_progress(painter, option, item)
                self._draw_sequence_flag(painter, option)
            else:
                q_image = self._image_server.get_image(item.current_filename)
            image = q_image or self._default_img
            image_rect = self._draw_centralized_pic(painter, option, image)
            if self._parent.show_asset_name:
                self._draw_text(painter, option, item.name)
            if self._parent.show_asset_flag:
                self._draw_stored_flag(painter, option, item)
                self._draw_description_flag(painter, option, item)
                self._draw_tag_flag(painter, option, item)
            if self._parent.paint_description:
                self._draw_description(painter, image_rect, item)
        finally:
            painter.restore()

    @staticmethod
    def draw_background(painter, option):
        """
        Draw the background for the item.

        :type painter: QtWidgets.QPainter
        :type option: QtWidgets.QStyleOptionViewItem
        :type index: QtCore.QModelIndex
        :rtype: None
        """
        rect = option.rect.adjusted(1, 1, -1, -1)
        is_selected = option.state & QStyle.State_Selected
        is_mouse_over = option.state & QStyle.State_MouseOver
        pen_color = mliber_config.BACKGROUND_COLOR
        pen = QPen()
        pen.setWidth(4)

        if is_selected:
            pen_color = QColor(57, 255, 255)
            pen.setWidth(2)
        elif is_mouse_over:
            pen_color = QColor(255, 255, 255, 75)
            pen.setWidth(2)

        pen.setColor(pen_color)
        painter.setPen(pen)
        painter.setBrush(QBrush(QColor(40, 40, 40, 100)))
        painter.drawRoundedRect(rect, 2, 2)

    def get_rect_margin(self):
        """
        get rect margin
        :return:
        """
        if self._parent.show_asset_flag and self._parent.show_asset_name:
            return [1, 20, -1, -20]
        else:
            if (not self._parent.show_asset_flag) and (not self._parent.show_asset_name):
                return [1, 0, -1, 0]
            elif self._parent.show_asset_flag and not self._parent.show_asset_name:
                return [1, 20, -1, 0]
            return [1, 0, -1, -20]

    def _draw_centralized_pic(self, painter, option, img):
        """
        画图
        :param painter:
        :param rect:
        :param img:
        :return:
        """
        rect_margin = self.get_rect_margin()
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
        return img_adjusted_rect

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
        is_selected = option.state & QStyle.State_Selected
        is_mouse_over = option.state & QStyle.State_MouseOver

        if is_selected or is_mouse_over:
            font = QFont("Arial", 8, QFont.Bold)
            painter.setFont(font)
            painter.setPen(QColor(255, 255, 255))
            text_rect = QRect(rect.adjusted(0, 0, 0, -20).bottomLeft(), rect.bottomRight())
            painter.drawText(text_rect, Qt.AlignCenter, text)

    @staticmethod
    def _draw_progress(painter, option, item):
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

    def _draw_sequence_flag(self, painter, option):
        """
        画序列标志
        :param painter:
        :param option:
        :return:
        """
        r = option.rect
        x = r.topRight().x() - 20 - PADDING
        y = r.y() + PADDING
        rect = QRect(x, y, 20, 20)
        painter.drawPixmap(rect, self._sequence_img)

    def _draw_stored_flag(self, painter, option, item):
        """
        画收藏标签
        :param painter:
        :param option:
        :return:
        """
        image = self._store_image_of_item(item)
        r = option.rect
        x = r.x() + PADDING
        y = r.y() + PADDING
        rect = QRect(x, y, FLAG_SIZE, FLAG_SIZE)
        painter.drawPixmap(rect, image)

    def _draw_description_flag(self, painter, option, item):
        """
        画收藏标签
        :param painter:
        :param option:
        :return:
        """
        image = self._description_image_of_item(item)
        r = option.rect
        x = r.x() + FLAG_SIZE + PADDING
        y = r.y() + PADDING
        rect = QRect(x, y, 14, 14)
        painter.drawPixmap(rect, image)

    def _draw_tag_flag(self, painter, option, item):
        """
        画收藏标签
        :param painter:
        :param option:
        :return:
        """
        image = self._tag_image_of_item(item)
        r = option.rect
        x = r.x() + (FLAG_SIZE + PADDING) * 2
        y = r.y() + PADDING
        rect = QRect(x, y, 14, 14)
        painter.drawPixmap(rect, image)

    def _draw_description(self, painter, rect, item):
        """
        将资产描述打印在图片上
        :return:
        """
        font = QFont("Arial", self._parent.paint_size, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QColor(*self._parent.paint_color))
        flags = Qt.AlignBottom | Qt.AlignHCenter | Qt.TextWordWrap
        painter.drawText(rect, flags, item.description)
