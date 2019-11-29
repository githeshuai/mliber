# -*- coding:utf-8 -*-
import mliber_global
from mliber_qt_components.image_sequence_widget import ImageSequence


class AssetListItem(object):
    def __init__(self, asset, parent):
        """
        :param asset: <Asset>
        :param parent: QListView
        """
        self.asset = asset
        self._parent = parent
        self.row = None
        self.image_sequence = None
        self.image_sequence_dir = None
        self.current_filename = None
        self.started = False
        self.has_sequence = False
        self.icon_size = self._parent.iconSize()
        self.has_tag = True if self.asset.tags else False
        self.has_description = True if self.asset.description else False
        self.stored_by_me = self.is_stored_by_me()

    def start(self):
        """
        start
        :return:
        """
        self.image_sequence.start()
        index = self._parent.model().index(self.row, 0)
        src_index = self._parent.model().mapToSource(index)
        self._parent.model().sourceModel().setData(src_index, ["started", True])

    def pause(self):
        """
        pause
        :return:
        """
        self.image_sequence.pause()
        index = self._parent.model().index(self.row, 0)
        src_index = self._parent.model().mapToSource(index)
        self._parent.model().sourceModel().setData(src_index, ["started", False])

    def set_image_sequence(self, sequence_dir):
        """
        set image sequence
        :return:
        """
        self.image_sequence = ImageSequence()
        self.image_sequence.setDirname(sequence_dir)
        self.image_sequence_dir = sequence_dir
        self.current_filename = self.image_sequence.currentFilename()
        self.image_sequence.frameChanged.connect(self._frame_changed)
        self.has_sequence = self.image_sequence.hasSequence()

    def _frame_changed(self):
        """

        :return:
        """
        self.current_filename = self.image_sequence.currentFilename()
        self._parent.repaint()

    def central_frame(self):
        """
        中间帧
        :return:
        """
        return self.image_sequence.centralFrame()

    def is_stored_by_me(self):
        """
        是否被自己收藏
        :return:
        """
        favorites = self.asset.favorite
        if favorites:
            user_ids = [favorite.user_id for favorite in favorites if favorite.status == "Active"]
            user = mliber_global.user()
            if user.id in user_ids:
                return True
        return False

    def __getattr__(self, item):
        """
        :param item:
        :return:
        """
        if item == "path":
            root_path = self.asset.library.root_path()
            return self.asset.path.format(root=root_path)
        return getattr(self.asset, item)
