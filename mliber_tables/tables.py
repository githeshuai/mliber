# -*- coding:utf-8 -*-
from mliber_lib.sql_lib.sql import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship


class User(Base):
    """
    用户表
    """
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), unique=True, nullable=False)
    chinese_name = Column(String(20))
    password = Column(String(20), default="123456")
    created_at = Column(DateTime)
    created_by = Column(Integer)
    user_permission = Column(Boolean, default=0)
    library_permission = Column(Boolean, default=0)
    category_permission = Column(Boolean, default=1)
    asset_permission = Column(Boolean, default=1)
    tag_permission = Column(Boolean, default=1)
    status = Column(Enum("Active", "Disable"))
    description = Column(Text)
    # relationship
    assets = relationship("Asset", backref="master", secondary="store")   # 与收藏资产的管理
    

class Library(Base):
    """
    库表
    """
    __tablename__ = "library"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), unique=True, nullable=False)
    type = Column(String(20), nullable=False)
    created_at = Column(DateTime)
    windows_path = Column(Text, unique=True)
    linux_path = Column(Text, unique=True)
    mac_path = Column(Text, unique=True)
    description = Column(Text)
    # foreign key
    user_id = Column(Integer, ForeignKey("user.id"))   # created by
    # relation ship
    categories = relationship("Category", backref="library")


class Category(Base):
    """
    分类表
    """
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    parent_id = Column(Integer)
    created_at = Column(DateTime)
    description = Column(Text)
    path = Column(Text)
    # foreign key
    library_id = Column(Integer, ForeignKey("library.id"))
    user_id = Column(Integer, ForeignKey("user.id"))  # created by
    # relation ship
    assets = relationship("Asset", backref="category")


class Asset(Base):
    """
    资产表
    """
    __tablename__ = "asset"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    created_at = Column(DateTime)
    description = Column(Text)
    path = Column(Text)
    # foreign key
    category_id = Column(Integer, ForeignKey("category.id"))
    user_id = Column(Integer, ForeignKey("user.id"))  # created by
    # relation ship
    objects = relationship("LiberObject", backref="asset")
    tags = relationship("Tag", backref="assets", secondary="asset_tag_link")


class LiberObject(Base):
    """
    导出的东西表
    """
    __tablename__ = "liberobject"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    type = Column(String(20))
    created_at = Column(DateTime)
    description = Column(Text)
    software = Column(Text)
    plugin = Column(Text)
    path = Column(Text)
    # foreign key
    asset_id = Column(Integer, ForeignKey("asset.id"))
    user_id = Column(Integer, ForeignKey("user.id"))  # created by


class Tag(Base):
    """
    标签表
    """
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False, unique=True)
    created_at = Column(DateTime)
    description = Column(Text)
    # foreign key
    user_id = Column(Integer, ForeignKey("user.id"))  # created by


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
