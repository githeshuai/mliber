# -*- coding: utf-8 -*-
import json
import hou
from mliber_hook.base_hook import BaseHook
from mliber_libs.os_libs.path import Path


class Hook(BaseHook):
    def __init__(self, path, objects, start, end, asset_name, software, plugin):
        super(Hook, self).__init__(path, objects, start, end, asset_name, software, plugin)

    def execute(self, *args, **kwargs):
        parent_dir = Path(self.path).parent()
        json_path = Path(parent_dir).join("path.json")
        if Path(json_path).isfile():
            with open(json_path, 'r') as f:
                data = json.loads(f.read())
                hou.ui.displayMessage(data.get("path"))
        else:
            hou.ui.displayMessage("No path.json file found.")
