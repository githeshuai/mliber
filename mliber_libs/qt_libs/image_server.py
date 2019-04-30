# -*- coding: utf-8 -*-
import time
from Qt.QtCore import Signal, QThread, Qt, QSize, QObject
from Qt.QtGui import QImageReader


class ImageCacheThread(QThread):
    cache_done_signal = Signal(object)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.__img_dict = {}
        self.clear_img_dict()

    @staticmethod
    def load_image_from_disk(file_path):
        """
        load image from disk
        Args:
            file_path: <str> a file path
        Returns: QImage

        """
        reader = QImageReader()
        reader.setFileName(file_path)
        image_size = reader.size()
        image_size.scale(QSize(150, 150), Qt.KeepAspectRatio)
        reader.setScaledSize(image_size)
        image = reader.read()
        return image

    def update_img_dict(self, image_path):
        """
        Args:
            image_path: <str>
        Returns:
            img_dict ={
                'img_hash' : [True, QImage] # True: cached ,default is False
            }
        """
        temp_img_dict = {image_path: [False, None]}
        self.__img_dict.update(temp_img_dict)

    def clear_img_dict(self):
        self.__img_dict = {}

    def run(self):
        while 1:
            self.check_img_list()
            time.sleep(0.5)

    def check_img_list(self):
        for image_path, data in self.__img_dict.items():
            cached, item = data
            if not cached:
                # update the cache data
                _img_item = self.load_image_from_disk(image_path)
                self.cache_done_signal.emit(_img_item)
                self.__img_dict[image_path] = [True, _img_item]

    def get_img_cache(self, image_path):
        img_data = self.__img_dict.get(image_path, None)
        if img_data:
            cached, item = img_data
            if cached:
                return item
            else:
                return None
        else:
            self.update_img_dict(image_path)


class ImageCacheThreadsServer(QObject):
    cache_done_signal = Signal(object)

    def __init__(self, thread_count=3):
        super(ImageCacheThreadsServer, self).__init__()
        self._thread_count = thread_count
        self._img_list = []
        self.thread_pool = []
        for index in range(thread_count):
            self.thread_pool.append(ImageCacheThread())
            self.thread_pool[index].cache_done_signal.connect(self.cache_done_signal)
            self.thread_pool[index].start()

    def get_qimage(self, image_path):
        if not image_path:
            return
        if image_path not in self._img_list:
            self._img_list.append(image_path)
        image_index = self._img_list.index(image_path)
        cur_img_thread_index = image_index % self._thread_count
        return self.thread_pool[cur_img_thread_index].get_img_cache(image_path)

    def clear_img_cache(self):
        self._img_list = []
        for thread in self.thread_pool:
            thread.clear_img_dict()

    def __del__(self):
        for thread in self.thread_pool:
            try:
                thread.terminate()
            except Exception as e:
                pass
