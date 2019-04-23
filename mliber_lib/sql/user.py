# -*- coding:utf-8 -*-
from mliber_tables.tables import User


class MUser(object):
    def __init__(self, session):
        self.session = session

