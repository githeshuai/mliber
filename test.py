import random
import hashlib
import requests
import os
from PySide.QtCore import *
from PySide.QtGui import *
import time


def ensure_dir_existed(dir_path):
    if not os.path.isdir(dir_path):
        try:
            os.makedirs(dir_path)
        except:
            pass


def get_file_base_name(file_path):
    return os.path.basename(file_path)


def join_paths(*args):
    return os.path.join(*args).replace("\\", "/")


def get_dir_file_list(dir_path):
    file_path_list = []
    for root, folders, files in os.walk(dir_path):
        file_path_list += [join_paths(root, _file_item) for _file_item in files]
    return file_path_list


class ImageCacheThread(QThread):
    cache_done_signal = Signal(object)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.__img_dict = {}
        self.clear_img_dict()

    def load_qimage_from_disk(self, file_path):
        reader = QImageReader()
        reader.setFileName(file_path)
        image_size = reader.size()
        image_size.scale(QSize(500, 500), Qt.KeepAspectRatio)
        reader.setScaledSize(image_size)
        image = reader.read()
        return image

    def update_img_dict(self, img_path):
        """
            img_dict ={
                'img_hash' : [True,ImagePath,QImageItem] # True: cached ,default is False
            }
        """
        temp_img_dict = {
            img_path: [
                False,
                img_path,
                None
            ]
        }

        self.__img_dict.update(temp_img_dict)

    def clear_img_dict(self):
        self.__img_dict = {}

    def run(self):
        while 1:
            self.check_img_list()
            time.sleep(0.5)

    def check_img_list(self):
        for img_hash, data in self.__img_dict.items():
            cached, img_path, item = data
            if not cached:
                # update the cache data
                _img_item = self.load_qimage_from_disk(img_path)
                self.cache_done_signal.emit(_img_item)
                self.__img_dict[img_path] = [True, img_path, _img_item]

    def get_img_cache(self, img_path):
        img_data = self.__img_dict.get(img_path, None)
        if img_data:
            cached, img_path, item = img_data
            if cached:
                return item
            else:
                return None
        else:
            self.update_img_dict(img_path)


class ImageCacheThreadsServer(QObject):
    cache_done_signal = Signal(object)

    def __init__(self, thread_count=3):
        super(ImageCacheThreadsServer, self).__init__()
        self._thread_count = thread_count
        self._img_list = []
        self.thread_poll = []
        for index in range(thread_count):
            self.thread_poll.append(ImageCacheThread())
            self.thread_poll[index].cache_done_signal.connect(self.cache_done_signal)
            self.thread_poll[index].start()

    def get_img_cache(self, img_path):
        if img_path not in self._img_list:
            self._img_list.append(img_path)

        cur_img_thread_index = self._img_list.index(img_path) % self._thread_count
        return self.thread_poll[cur_img_thread_index].get_img_cache(img_path)

    def clear_img_cache(self):
        self._img_list = []
        for thread in self.thread_poll:
            thread.clear_img_dict()

    def __del__(self):
        for thread in self.thread_poll:
            thread.quit()


class FilesListModel(QAbstractListModel):
    def __init__(self, parent=None, view=None):
        super(FilesListModel, self).__init__(parent)
        self._pic_list = []
        self.__view = view
        self._app = QApplication.instance()

    def set_pic_list(self, pic_list):
        self._pic_list = pic_list
        self.__view.reset()
        # clear the img thread cache
        self.delegate._app_imag_cache_threads.clear_img_cache()

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole:
            return ""

    def rowCount(self, parent=QModelIndex()):
        return len(self._pic_list)


class FilesListDelegate(QItemDelegate):
    def __init__(self, parent=None, model=None):
        super(FilesListDelegate, self).__init__(parent)
        app = QApplication.instance()
        self._app_imag_cache_threads = app.image_cache_threads
        self._app_imag_cache_threads.cache_done_signal.connect(self._img_cached_done)
        self._cache = {}
        self.size_hint = QSize(150, 150)
        self._margin = 5
        self._water_print_scale_ratio = 0.2
        self._model = model
        self._model.delegate = self

    def _img_cached_done(self, img_item):
        self.parent().setUpdatesEnabled(False)
        self.parent().repaint()
        self.parent().setUpdatesEnabled(True)

    def paint(self, painter, option, index):
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, QColor(0, 0, 120, 140))

        row = index.row()
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        img_path = self._model._pic_list[row]

        img_item = self._app_imag_cache_threads.get_img_cache(img_path)
        # img_item in the dict ,don't know if cached
        if img_item:
            img_rect = self.draw_centrialized_pic(painter, option.rect, img_item)
            self.draw_text(painter, option.rect, get_file_base_name(self._model._pic_list[row]))
        else:
            pass

        if option.state & QStyle.State_Selected:
            painter.save()
            painter.setPen(Qt.yellow)
            painter.drawRect(option.rect)
            painter.restore()

    def draw_water_print(self, painter, rect, img):
        painter.save()
        src_rect = rect
        right, bottom = float(src_rect.width()), float(src_rect.height())
        img_width, img_height = float(img.width()), float(img.height())

        if img_width / img_height > 1:
            scale_ratio = img_width / right
        else:
            scale_ratio = img_height / bottom

        # final_rect = src_rect.adjusted(right * (1 - 1 / scale_ratio), bottom * (1 - 1 / scale_ratio), 0, 0)
        final_rect = src_rect.adjusted(right - 40, bottom - 40, 0, 0)
        painter.drawPixmap(final_rect, img)
        painter.restore()
        return final_rect

    def draw_centrialized_pic(self, painter, rect, img, rect_margin=[0, 0, 0, -20]):
        try:
            painter.save()
            img_rect = rect.adjusted(
                self._margin + rect_margin[0], self._margin + rect_margin[1],
                -self._margin + rect_margin[2], -self._margin + rect_margin[3]
            )
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
            painter.restore()
            return img_adjusted_rect
        except:
            return rect

    def draw_text(self, painter, rect, text):
        painter.save()
        # draw text
        font = QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(7)
        painter.setFont(font)
        painter.setPen(QColor(0, 160, 230))
        text_rect = QRect(rect.adjusted(10, 0, 0, -28).bottomLeft(), rect.bottomRight())
        painter.drawText(text_rect, Qt.AlignCenter, text)
        painter.restore()
        return text_rect

    def sizeHint(self, index, option):
        return self.size_hint


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    app.image_cache_threads = \
        ImageCacheThreadsServer(thread_count=10)

    ui = QListView()
    ui.setModel(FilesListModel(view=ui))

    ui_delegate = FilesListDelegate(ui, model=ui.model())
    ui.setItemDelegate(ui_delegate)

    ui.setViewMode(QListView.IconMode)
    ui.setSelectionMode(QListView.ExtendedSelection)
    ui.setResizeMode(QListView.Adjust)

    ui.model().set_pic_list(get_dir_file_list(r"D:\textures\image"))

    ui.show()
    ui.resize(1000, 1000)

    sys.exit(app.exec_())

