# -*- coding:utf-8 -*-
import re
import os
from Qt.QtWidgets import QToolButton, QApplication
from Qt.QtGui import QColor, QIcon, QPainter, QBrush, QPixmap
from Qt.QtCore import Signal, QObject, QSize, Qt, QTimer
import mliber_resource


__all__ = ['ImageSequence', 'ImageSequenceWidget']


class ImageSequence(QObject):
    DEFAULT_FPS = 24
    frameChanged = Signal()

    def __init__(self, *args):
        QObject.__init__(self, *args)
        self._fps = self.DEFAULT_FPS
        self._timer = None
        self._frame = 0
        self._frames = []
        self._dirname = None
        self._paused = False

    def setDirname(self, dirname):
        """
        Set the location to the image sequence.

        :type dirname: str
        :rtype: None
        """

        def naturalSortItems(items):
            """
            Sort the given list in the way that humans expect.
            """
            convert = lambda text: (int(text) if text.isdigit() else text)
            alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
            items.sort(key=alphanum_key)

        self._dirname = dirname
        if os.path.isdir(dirname):
            self._frames = [dirname + '/' + filename for filename in os.listdir(dirname)]
            naturalSortItems(self._frames)

    def centralFrame(self):
        """
        第一帧
        :return:
        """
        if self._frames:
            return self._frames[len(self._frames)/2]

    def dirname(self):
        """
        Return the location to the image sequence.

        :rtype: str
        """
        return self._dirname

    def reset(self):
        """
        Stop and reset the current frame to 0.

        :rtype: None
        """
        if not self._timer:
            self._timer = QTimer(self.parent())
            self._timer.setSingleShot(False)
            self._timer.timeout.connect(self._frameChanged)
        if not self._paused:
            self._frame = 0
        self._timer.stop()

    def pause(self):
        """
        ImageSequence will enter Paused state.

        :rtype: None
        """
        self._paused = True
        self._timer.stop()

    def resume(self):
        """
        ImageSequence will enter Playing state.

        :rtype: None
        """
        if self._paused:
            self._paused = False
            self._timer.start()

    def stop(self):
        """
        Stops the movie. ImageSequence enters NotRunning state.

        :rtype: None
        """
        self._frame = 0
        self._timer.stop()

    def start(self):
        """
        Starts the movie. ImageSequence will enter Running state

        :rtype: None
        """
        self.reset()
        if self._timer:
            self._timer.start(1000.0 / self._fps)

    def frames(self):
        """
        Return all the filenames in the image sequence.

        :rtype: list[str]
        """
        return self._frames

    def _frameChanged(self):
        """
        Triggered when the current frame changes.

        :rtype: None
        """
        if not self._frames:
            return
        frame = self._frame
        frame += 1
        self.setCurrentFrame(frame)

    def percent(self):
        """
        Return the current frame position as a percentage.

        :rtype: None
        """
        if len(self._frames) == self._frame + 1:
            _percent = 1
        else:
            _percent = float(len(self._frames) + self._frame) / len(self._frames) - 1
        return _percent

    def duration(self):
        """
        Return the number of frames.

        :rtype: int
        """
        return len(self._frames)

    def currentFilename(self):
        """
        Return the current file name.

        :rtype: str or None
        """
        try:
            return self._frames[self.currentFrame()]
        except IndexError:
            pass

    def currentFrame(self):
        """
        Return the current frame.

        :rtype: int or None
        """
        return self._frame

    def setCurrentFrame(self, frame):
        """
        Set the current frame.

        :rtype: int or None
        """
        if frame >= self.duration():
            frame = 0
        self._frame = frame
        self.frameChanged.emit()


class ImageSequenceWidget(QToolButton):
    DEFAULT_PLAYHEAD_COLOR = QColor(180, 180, 180, 200)

    def __init__(self, parent=None):
        super(ImageSequenceWidget, self).__init__(parent)
        self.setStyleSheet("border: 0px solid; padding: 0px; background: #8a8a8a;")
        self._filename = None
        self._imageSequence = ImageSequence(self)
        self._imageSequence.frameChanged.connect(self._frameChanged)
        self._sequencePixMap = self.sequencePixMap()
        self._defaultIconPath = mliber_resource.icon("image.png")
        self.setMouseTracking(True)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

    def hasSequence(self):
        """
        判断缩略图是否有序列
        :return:
        """
        return True if self._imageSequence.duration() > 1 else False

    def isControlModifier(self):
        """
        :rtype: bool
        """
        modifiers = QApplication.keyboardModifiers()
        return modifiers == Qt.ControlModifier

    def setSize(self, size):
        """
        Reimplemented so that the icon size is set at the same time.
        :rtype: None
        """
        self._size = size
        self.setIconSize(self._size)
        self.setFixedSize(self._size)

    def currentIcon(self):
        """
        Return a icon object from the current icon path.

        :rtype: QIcon
        """
        return QIcon(self._imageSequence.currentFilename())

    def setDirname(self, dirname):
        """
        Set the location to the image sequence.

        :type dirname: str
        :rtype: None
        """
        self._imageSequence.setDirname(dirname)

    def enterEvent(self, event):
        """
        Start playing the image sequence when the mouse enters the widget.

        :type event: QEvent
        :rtype: None
        """
        self._imageSequence.start()

    def leaveEvent(self, event):
        """
        Stop playing the image sequence when the mouse leaves the widget.

        :type event: QEvent
        :rtype: None
        """
        self._imageSequence.pause()

    def mouseMoveEvent(self, event):
        """
        Reimplemented to add support for scrubbing.

        :type event: QEvent
        :rtype: None
        """
        if self.isControlModifier():
            percent = 1.0 - float(self.width() - event.pos().x()) / float(self.width())
            frame = int(self._imageSequence.duration() * percent)
            self._imageSequence.setCurrentFrame(frame)
            icon = self.currentIcon()
            self.setIcon(icon)

    def _frameChanged(self, filename=None):
        """
        Triggered when the image sequence changes frame.

        :type filename: str or None
        :rtype: None
        """
        if not self.isControlModifier():
            self._filename = filename
            icon = self.currentIcon()
            self.setIcon(icon)

    def currentFilename(self):
        """
        Return the current image location.

        :rtype: str
        """
        return self._imageSequence.currentFilename()

    def playheadHeight(self):
        """
        Return the height of the playhead.

        :rtype: int
        """
        return 2

    def sequecneFlagWidth(self):
        """
        sequence 图标的尺寸
        :return:
        """
        return 20

    def sequencePixMap(self):
        """
        序列图标
        :return:
        """
        pixmap = QPixmap(mliber_resource.icon_path("video.png"))
        pixmap_size = QSize(self.sequecneFlagWidth(), self.sequecneFlagWidth())
        scaled_pixmap = pixmap.scaled(pixmap_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return scaled_pixmap

    def paintEvent(self, event):
        """
        Triggered on frame changed.

        :type event: QEvent
        :rtype: None
        """
        QToolButton.paintEvent(self, event)
        if not self.hasSequence():
            return
        else:
            painter = QPainter()
            r = event.rect()
            painter.begin(self)
            painter.drawPixmap(r.width() - self.sequecneFlagWidth(), 0, self._sequencePixMap)
            if self.currentFilename():
                playheadHeight = self.playheadHeight()
                playheadPosition = self._imageSequence.percent() * r.width()
                x = r.x()
                y = self.height() - playheadHeight
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(QColor(200, 150, 50)))
                painter.drawRect(x, y, playheadPosition, playheadHeight)
            painter.end()

    def mousePressEvent(self, event):
        self.deleteLater()
        event.ignore()


if __name__ == '__main__':

    app = QApplication([])
    w = ImageSequenceWidget(None)
    w.setDirname(r'D:\textures\sequence\dst')
    w.show()
    app.exec_()
