# -*- coding: utf-8 -*-
# Auther: Henry
# Email: 17607168727@163.com
import configparser


def get_config(section, key):
    """
    获取配置
    """
    config = configparser.ConfigParser()
    path = '../conf/default.conf'
    config.read(path)
    return config.get(section, key)


def set_config(section, key, value):
    """
    写入配置
    """
    config = configparser.ConfigParser()
    path = '../conf/default.conf'
    config.read(path)
    config.set(section, key, value)
    with open(path, 'w') as fw:  # 循环写入
        config.write(fw)
