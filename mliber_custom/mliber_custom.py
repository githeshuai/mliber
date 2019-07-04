# -*- coding:utf-8 -*-
# 数据库配置
# DATABASE的key指的是数据库的名字，就是显示在登录界面上，让用户选择使用哪个数据库
# TYPE: 数据库类型，只支持sqlite, mysql, postgresql
# ENGINE: 连接数据库的engine,  熟悉sqlalchemy的朋友知道engine概念，默认就是数据库的类型
# PATH: 指的是sqlite的.db文件存放路径
# NAME: 指的是数据库的名字，就是CREATE DATABASE {数据库名字}
# USER: 登录数据库的用户名
# HOSE: 数据库部署的IP地址
# PASSWORD： 数据库访问密码

DATABASES = {

    'sqlite': {
        "TYPE": "sqlite",
        "ENGINE": "sqlite",
        "PATH": "D:/test.db"
    },

    'mysql': {
        "TYPE": "mysql",
        "ENGINE": "mysql",
        'NAME': "test",
        "USER": "root",
        "HOST": "192.168.202.128",
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

}


# 公共路径配置
# 该路径为公共路径，用来存放用户自定义的图片（比如library icon....）
# 注意： 该路径一定要是所有人都有777的权限。
PUBLIC_PATH = {
    "windows": "D:/mliber_repo",
    "linux": "/media/X/mliber_repo",
    "mac": ""
}

# hook 路径
# 如果此处为空，默认路径为/mliber/mliber_hook
HOOK_DIR = []


# 缩略图的最大尺寸
THUMBNAIL_SIZE = 256


# 是否将描述打印在资产上
PAINT_DESCRIPTION = True                # 是否将描述打印在资产图片上
DESCRIPTION_COLOR = [255, 255, 0]       # 打印描述的颜色
DESCRIPTION_FONT_SIZE = 10              # 打印描述的字体大小
