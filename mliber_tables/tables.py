# -*- coding:utf-8 -*-
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from Qt.QtGui import QColor
from mliber_libs.sql_libs.sql import Base
from mliber_libs.os_libs import system


def this_moment():
    now = datetime.now()
    return now


class User(Base):
    """
    用户表
    """
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), unique=True, nullable=False)
    chinese_name = Column(String(20))
    password = Column(String(20), default="123456")
    created_at = Column(DateTime, default=this_moment())
    updated_at = Column(DateTime)
    created_by = Column(Integer)
    updated_by = Column(Integer)
    user_permission = Column(Boolean, default=0)
    library_permission = Column(Boolean, default=0)
    category_permission = Column(Boolean, default=1)
    asset_permission = Column(Boolean, default=1)
    tag_permission = Column(Boolean, default=1)
    status = Column(Enum("Active", "Disable"), default="Active")
    description = Column(Text)
    # relationship
    assets = relationship("Asset", backref="master", secondary="store")   # 与收藏资产的管理

    def __str__(self):
        return self.name
    

class Library(Base):
    """
    库表
    """
    __tablename__ = "library"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=this_moment())
    updated_at = Column(DateTime)
    windows_path = Column(String(300))
    linux_path = Column(String(300))
    mac_path = Column(String(300))
    description = Column(Text)
    status = Column(Enum("Active", "Disable"), default="Active")
    # foreign key
    created_by = Column(Integer, ForeignKey("user.id"))   # created by
    updated_by = Column(Integer, ForeignKey("user.id"))
    # relation ship
    categories = relationship("Category", backref="library")
    assets = relationship("Asset", backref="library")

    def __str__(self):
        return self.name

    def root_path(self):
        """
        根据当前系统获取
        :return:
        """
        current_system = system.operation_system()
        path_str = "{}_path".format(current_system)
        return getattr(self, path_str)


class Category(Base):
    """
    分类表
    """
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    parent_id = Column(Integer)
    created_at = Column(DateTime, default=this_moment())
    updated_at = Column(DateTime)
    description = Column(Text)
    path = Column(Text)
    status = Column(Enum("Active", "Disable"), default="Active")
    # foreign key
    library_id = Column(Integer, ForeignKey("library.id"))
    created_by = Column(Integer, ForeignKey("user.id"))  # created by
    updated_by = Column(Integer, ForeignKey("user.id"))
    # relation ship
    assets = relationship("Asset", backref="category")

    def __str__(self):
        return self.name


class Asset(Base):
    """
    资产表
    """
    __tablename__ = "asset"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(300), nullable=False)
    created_at = Column(DateTime, default=this_moment())
    updated_at = Column(DateTime)
    description = Column(Text)
    path = Column(Text)
    status = Column(Enum("Active", "Disable"), default="Active")
    # foreign key
    library_id = Column(Integer, ForeignKey("library.id"))
    category_id = Column(Integer, ForeignKey("category.id"))
    created_by = Column(Integer, ForeignKey("user.id"))  # created by
    updated_by = Column(Integer, ForeignKey("user.id"))
    # relation ship
    elements = relationship("Element", backref="asset")
    tags = relationship("Tag", backref="assets", secondary="asset_tag_link")

    def __str__(self):
        return self.name.encode("utf-8")


class Tag(Base):
    """
    标签表
    """
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(300), nullable=False, unique=True)
    created_at = Column(DateTime, default=this_moment())
    updated_at = Column(DateTime)
    description = Column(Text)
    status = Column(Enum("Active", "Disable"), default="Active")
    # foreign key
    created_by = Column(Integer, ForeignKey("user.id"))  # created by
    updated_by = Column(Integer, ForeignKey("user.id"))
    # color
    colorR = Column(Integer, default=138)
    colorG = Column(Integer, default=138)
    colorB = Column(Integer, default=138)

    def __str__(self):
        return self.name

    def color(self):
        """
        get color
        :return: QColor
        """
        return QColor(self.colorR, self.colorG, self.colorB)


class Element(Base):
    """
    导出的东西表
    """
    __tablename__ = "element"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(300), nullable=False)
    type = Column(String(50))
    created_at = Column(DateTime, default=this_moment())
    updated_at = Column(DateTime)
    description = Column(Text)
    software = Column(Text)
    plugin = Column(Text)
    start = Column(Integer, default=1)
    end = Column(Integer, default=1)
    path = Column(Text)
    status = Column(Enum("Active", "Disable"), default="Active")
    # foreign key
    asset_id = Column(Integer, ForeignKey("asset.id"))
    created_by = Column(Integer, ForeignKey("user.id"))  # created by
    updated_by = Column(Integer, ForeignKey("user.id"))

    def __str__(self):
        return self.name


class AssetTagLink(Base):
    """
    资产和标签链接表
    """
    __tablename__ = "asset_tag_link"
    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(Integer, ForeignKey("asset.id"))
    tag_id = Column(Integer, ForeignKey("tag.id"))


class Store(Base):
    """
    个人收藏链接
    """
    __tablename__ = "store"
    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(Integer, ForeignKey("asset.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
