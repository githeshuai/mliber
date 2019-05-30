# -*- coding:utf-8 -*-

DATABASES = {
    'default': {
        "TYPE": "mysql",
        "ENGINE": "mysql",
        'NAME': "test",
        "USER": "root",
        "HOST": "192.168.137.130",
        "PASSWORD": "Digisky_2019",
    },

    'postgresql': {
        "TYPE": "postgresql",
        "ENGINE": "postgresql",
        'NAME': "test",
        "USER": "root",
        "HOST": "192.168.137.128",
        "PASSWORD": "Digisky_2019",
    },

    'sqlite': {
        "TYPE": "sqlite",
        "ENGINE": "sqlite",
        "PATH": "D:/test.db"
    },
}
