# -*- coding:utf-8 -*-
from mliber_tables.tables import User


class MUser(object):
    def __init__(self, session):
        self.session = session

    def create(self, name, chinese_name, created_by, password="123456", user_permission=False, library_permission=False,
               category_permission=False, asset_permission=True, tag_permission=True, status="Active", description=""):
        """
        创建用户
        :param created_by:
        :return:
        """
        user = User(name=name, chinese_name=chinese_name, created_by=created_by, password=password,
                    user_permission=user_permission, library_permission=library_permission,
                    category_permission=category_permission, asset_permission=asset_permission,
                    tag_permission=tag_permission, status=status, description=description)
        self.session.add(user)
        self.session.commit()



