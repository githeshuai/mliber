# -*- coding:utf-8 -*-
from Qt.QtGui import QColor

# when get children file, ignore the files
IGNORE_LIST = [".", "Thumbs.db", ".mayaSwatches", ".nk~", ".autosave"]

# 配置视频格式
VIDEO_EXT = [".mov", ".mp4", ".avi", ".gif", ".mkv"]

# font name
FONT_NAME = "Arial"
# COLOR
BACKGROUND_COLOR = "#40444f"
TITLE_COLOR = "#373b44"
MENU_COLOR = "#2d2f37"
# button icon color
ICON_COLOR = QColor(160, 160, 160)
ICON_HOVER_COLOR = QColor(57, 255, 255)
ACCENT_COLOR = "rgb(57, 255, 255)"

# comments color
COMMENTS_COLOR = QColor(255, 255, 0)

# BLUE COLOR
BLUE_COLOR = "#20A0FF"

# RED COLOR
RED_COLOR = "#f65150"

# ORANGE COLOR
ORANGE_COLOR = "#FF8C00"

# TAG DEFAULT COLOR
TAG_COLOR_R = 128
TAG_COLOR_G = 128
TAG_COLOR_B = 128


# delegate list view style
LIST_VIEW_STYLE = "QListView::item{background: #393c46;border-radius: 0px;}" \
                  "QListView::item:selected {background: #29475a; border: 1px solid #00b4ff; border-radius: 0px;}" \
                  "QListView::item:hover {background: #345f71; border-radius: 0px;}"\
                  "QListView::item:selected:!active {background: #29475a;}" \
                  "QListView::item:selected:active {background: #29475a;}"


# maya texture node and attr name mapping
TEXTURE_NODE_ATTR_DICT = {"file": "fileTextureName",
                          "RedshiftNormalMap": "tex0",
                          "RedshiftDomeLight": "tex0",
                          "aiImage": "filename",
                          "RedshiftIESLight": "profile",
                          "RedshiftSprite": "tex0"}


# maya color space node name and attr mapping
COLOR_SPACE_ATTR_DICT = {"file": "cs",
                         "aiImage": "cs"}