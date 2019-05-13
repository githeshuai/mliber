# -*- coding:utf-8 -*-
import re
import os
from PySide.QtGui import *
from PySide.QtCore import *

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
            self.connect(self._timer, SIGNAL('timeout()'), self._frameChanged)
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
    DEFAULT_PLAYHEAD_COLOR = QColor(255, 0, 0, 220)

    def __init__(self, *args):
        QToolButton.__init__(self, *args)
        self.setStyleSheet('border: 0px solid rgb(0, 0, 0, 20);')
        self._filename = None
        self._imageSequence = ImageSequence(self)
        self._imageSequence.frameChanged.connect(self._frameChanged)
        self.setSize(300, 300)
        self.setMouseTracking(True)

    def isControlModifier(self):
        """
        :rtype: bool
        """
        modifiers = QApplication.keyboardModifiers()
        return modifiers == Qt.ControlModifier

    def setSize(self, w, h):
        """
        Reimplemented so that the icon size is set at the same time.

        :type w: int
        :type h: int
        :rtype: None
        """
        self._size = QSize(w, h)
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
        if self._imageSequence.frames():
            icon = self.currentIcon()
            self.setIcon(icon)

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
        return 4

    def paintEvent(self, event):
        """
        Triggered on frame changed.

        :type event: QEvent
        :rtype: None
        """
        QToolButton.paintEvent(self, event)
        painter = QPainter()
        painter.begin(self)
        if self.currentFilename():
            r = event.rect()
            playheadHeight = self.playheadHeight()
            playheadPosition = self._imageSequence.percent() * r.width() - 1
            x = r.x()
            y = self.height() - playheadHeight
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(self.DEFAULT_PLAYHEAD_COLOR))
            painter.drawRect(x, y, playheadPosition, playheadHeight)
        painter.end()


if __name__ == '__main__':

    app = QApplication([])
    w = ImageSequenceWidget(None)
    w.setDirname(r'D:\asset_library\test\machine\computer\linux\redhat7')
    w.show()
    app.exec_()