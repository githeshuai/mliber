# -*- coding: utf-8 -*-
"""
parse /mliber_conf/element_type/{element_type}.yml
"""
import mliber_utils
from mliber_libs.os_libs.path import Path
from mliber_parse.action import Action


class ElementType(object):
    pool = dict()
    __init = False

    def __new__(cls, element_type=""):
        obj = cls.pool.get(element_type, None)
        if not obj:
            obj = object.__new__(cls)
            cls.pool[element_type] = obj
        return obj

    def __init__(self, element_type=""):
        """
        init
        :param element_type: <str> element type
        """
        if not self.__init:
            self._type = element_type
            self._data = self.parse()
            self.__init = True

    def element_type_conf_path(self):
        """
        获取配置文件路径
        :return:
        """
        path = "element_types/%s.yml" % self._type
        return path

    def parse(self):
        """
        get conf data
        :return:
        """
        return mliber_utils.parse(self.element_type_conf_path())

    def actions_of_engine(self, engine):
        """
        当前软件的所有action, 包括import和export
        :return: <dict>
        """
        if not self._data. has_key(engine):
            # print u"Software: %s not support type: %s" % (engine, self._type)
            return {}
        engine_actions = self._data.get(engine)
        return engine_actions

    def export_action_of_engine(self, engine):
        """
        export actions
        :return: <list>
        """
        engine_actions = self.actions_of_engine(engine)
        if engine_actions:
            action = engine_actions.get("export", {})
            if action:
                action.update({"type": self._type})
                return Action(action)
        return None

    def import_actions_of_engine(self, engine):
        """
        import actions
        :return:
        """
        engine_actions = self.actions_of_engine(engine)
        if engine_actions:
            export_action_list = engine_actions.get("import", [])
            if export_action_list:
                actions = [Action(action) for action in export_action_list]
                return actions
        return []

    def __getattr__(self, item):
        """

        :param item:
        :return:
        """
        if not self._data:
            # print "[MLIBER] warning: unknown element type: %s." % self._type
            return
        if item == "icon":
            icon = self._data.get("icon")
            icon_dir = mliber_utils.package("mliber_icons")
            if not icon:
                return Path(icon_dir).join("element_type_icons/default.png")
            if Path(icon).isfile():
                return icon
            icon = Path(icon_dir).join("element_type_icons/%s" % icon)
            if not Path(icon).isfile():
                icon = Path(icon_dir).join("element_type_icons/default.png")
            return icon
        return self._data.get(item, None)


if __name__ == "__main__":
    p = ElementType("ma").actions_of_engine("maya")
    print p
