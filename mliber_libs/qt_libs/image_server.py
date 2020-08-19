# -*- coding: utf-8 -*-
import time
import threading
from Qt.QtCore import Signal, QThread, Qt, QSize, QObject
from Qt.QtGui import QImageReader, QIcon, QPixmap

THREAD_COUNT = 10


class ImageItem(object):
    def __init__(self, image_path):
        self._image_path = image_path
        self._q_image = None

    @property
    def image_path(self):
        return self._image_path

    def is_cached(self):
        return True if self._q_image else False

    @property
    def q_image(self):
        return self._q_image

    def get_q_image(self):
        """
        load image from disk
        Returns: QIcon
        """
        reader = QImageReader()
        reader.setFileName(self._image_path)
        # image_size = reader.size()
        # image_size.scale(QSize(150, 150), Qt.KeepAspectRatio)
        # reader.setScaledSize(image_size)
        image = reader.read()
        self._q_image = image

    def update(self):
        self._q_image = None


class ImageCacheThread(QThread):
    cache_done_signal = Signal()

    def __init__(self):
        super(ImageCacheThread, self).__init__()
        self._cache_dict = dict()  # image_path: ImageItem

        self._lock = threading.Lock()
        self._stop = False

    def get_image_cache(self, image_path):
        """
        获取image cache
        :return:
        """
        if image_path in self._cache_dict:
            image_item = self._cache_dict.get(image_path)
            return image_item.q_image
        else:
            self.append_image(image_path)

    def append_image(self, image_path):
        """
        将文件添加到cache列表中
        :param image_path:
        :return:
        """

        image_item = ImageItem(image_path)
        self._cache_dict.update({image_path: image_item})

    def run(self):
        while not self._stop:
            for image_path in self._cache_dict:
                item = self._cache_dict.get(image_path)
                if not item.is_cached():
                    item.get_q_image()
                    self.cache_done_signal.emit()
            time.sleep(0.5)

    def update(self, image_path):
        item = self._cache_dict.get(image_path)
        if not item:
            self.append_image(image_path)
        else:
            item.update()

    def clear(self):
        self._cache_dict = dict()

    def stop(self):
        self._stop = True


class ImageCacheThreadsServer(QObject):
    cache_done_signal = Signal()

    def __init__(self, thread_count=THREAD_COUNT):
        super(ImageCacheThreadsServer, self).__init__()

        self._lock = threading.Lock()
        self._thread_count = thread_count
        self._image_list = []
        self._thread_pool = []
        for index in range(thread_count):
            self._thread_pool.append(ImageCacheThread())
            
        for thread in self._thread_pool:
            thread.cache_done_signal.connect(self.cache_done_signal)
            thread.start()

    def get_image(self, image_path):
        """
        从缓存序列中获取
        :param image_path:
        :return:
        """
        if not image_path:
            return
        try:
            self._lock.acquire()
            if image_path not in self._image_list:
                self._image_list.append(image_path)

            image_index = self._image_list.index(image_path)
            cur_img_thread_index = image_index % self._thread_count
            return self._thread_pool[cur_img_thread_index].get_image_cache(image_path)

        finally:
            self._lock.release()

    def update(self, image_path):
        """
        更新当前图
        :param image_path:
        :return:
        """
        if not image_path:
            return
        if image_path not in self._image_list:
            self._image_list.append(image_path)
        image_index = self._image_list.index(image_path)
        cur_img_thread_index = image_index % self._thread_count
        self._thread_pool[cur_img_thread_index].update(image_path)

    def clear(self):
        """
        清空线程
        :return:
        """
        self._image_list = []
        for thread in self._thread_pool:
            thread.clear()

    def __del__(self):
        self.close()

    def close(self):
        if self._thread_pool:
            for thread in self._thread_pool:
                thread.stop()


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication, QDialog
    app = QApplication([])
    dialog = QDialog()
    dialog.image_server = ImageCacheThreadsServer()
    dialog.show()
    dialog.image_server.close()  # must close all thread.
    sys.exit(app.exec_())
