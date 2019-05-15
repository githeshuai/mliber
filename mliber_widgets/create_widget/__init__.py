# -*- coding:utf-8 -*-
import os
import pprint
import pkgutil
import importlib
from create_widget import CreateWidget

pkg_dir = os.path.dirname(__file__)

for (module_loader, name, is_pkg) in pkgutil.iter_modules([pkg_dir]):
    importlib.import_module('.' + name, __package__)

classes = {cls.__name__: cls for cls in CreateWidget.__subclasses__()}
