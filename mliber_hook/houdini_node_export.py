# -*- coding: utf-8 -*-
from mliber_hook.base_hook import BaseHook
from mliber_libs.os_libs.path import Path
import json


class Hook(BaseHook):
    def __init__(self, path, objects, start, end, asset_name, software, plugin):
        super(Hook, self).__init__(path, objects, start, end, asset_name, software, plugin)
        self._parent_node = self.objects[0].parent()

    def execute(self, *args, **kwargs):
        self._parent_node.saveItemsToFile(self.objects, self.path)
        self.write_out_node_path()
        return self.path

    def write_out_node_path(self):
        """
        将当前路径写出
        :return:
        """
        parent_dir = Path(self.path).parent()
        meta_data_path = Path(parent_dir).join("path.json")
        meta_data = {"path": self._parent_node.path()}
        with open(meta_data_path, 'w') as f:
            json_data = json.dumps(meta_data)
            f.write(json_data)
