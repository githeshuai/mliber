# -*- coding: utf-8 -*-
import os
import json
import yaml


class YamlParser(object):
    def __init__(self, path):
        self.path = path

    def load(self):
        if not os.path.isfile(self.path):
            return None
        with open(self.path, "r") as f:
            data = yaml.load(f)
            return data

    def dump(self, data):
        yaml_dir = os.path.dirname(self.path)
        if not os.path.isdir(yaml_dir):
            os.makedirs(yaml_dir)
        with open(self.path, "w") as f:
            yaml.dump(data, f)

    def update(self, **kwargs):
        current_data = self.load()
        current_data.update(kwargs)
        self.dump(current_data)


class JsonParser(object):
    def __init__(self, path):
        self.path = path

    def load(self):
        if os.path.isfile(self.path):
            with open(self.path, 'r') as f:
                data = json.loads(f.read())
                return data
        else:
            return None

    def dump(self, data):
        json_dir = os.path.dirname(self.path)
        if not os.path.isdir(json_dir):
            os.makedirs(json_dir)
        with open(self.path, 'w') as f:
            json_data = json.dumps(data)
            f.write(json_data)

    def update(self, **kwargs):
        current_data = self.load()
        current_data.update(kwargs)
        self.dump(current_data)


class Parser(object):
    def __init__(self, path):
        self.path = path.replace("\\", "/")

    def parse(self):
        parser = None
        ext = os.path.splitext(self.path)[-1]
        if ext == ".json":
            parser = JsonParser(self.path)
        elif ext == ".yml":
            parser = YamlParser(self.path)
        else:
            print "add parser -.-"
        return parser


if __name__ == "__main__":
    cp = Parser(r"E:\MORE_WORKSPACE_MANAGER\conf\task_fields.yml")
    print cp.parse().load()
