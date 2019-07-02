# -*- coding:utf-8 -*-
import logging


class DccFactory(object):
    def __init__(self, engine):
        self._engine = engine

    def create(self):
        if self._engine == "maya":
            from _maya import Maya
            dcc_instance = Maya()
        elif self._engine == "nuke":
            from _nuke import Nuke
            dcc_instance = Nuke()
        elif self._engine == "houdini":
            from _houdini import Houdini
            dcc_instance = Houdini()
        elif self._engine == "clarisse":
            from _clarisse import Clarisse
            dcc_instance = Clarisse()
        elif self._engine == "unreal":
            from _unreal import Unreal
            dcc_instance = Unreal()
        else:
            if self._engine != "standalone":
                logging.warning("%s not supported" % self._engine)
            return
        return dcc_instance
