# -*- coding: utf-8 -*-
# Auther: Henry
# Email: 17607168727@163.com

import logging
from logging.handlers import RotatingFileHandler
from manage_config import get_config
import os.path


# 检测日志目录
log_path = get_config("log", "log_data")
dir_name = os.path.dirname(log_path)
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

# 实例化logging
logger = logging.getLogger("get_ip")
# 设置logger日志级别
logger.setLevel(level=logging.INFO)
# 实例化 日志格式对象
format = '%(asctime)s - %(module)s - %(levelname)s : %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(format, datefmt)

# 实例化 文件轮询日志处理器
# 第三个参数是日志文件的最大容量,单位是byte,换算单位以后是100M
# 第四个参数是轮换的次数
get_wan_ip_file_handler = RotatingFileHandler(get_config("log", "log_data"),
                                   'a',
                                   int(get_config("log", "max_Bytes")),
                                   get_config("log", "backup_count")
                                   )
# 设置 日志级别过滤器
get_wan_ip_file_handler.setLevel(logging.INFO)
# 设置 日志格式
get_wan_ip_file_handler.setFormatter(formatter)


# 实例化 终端日志处理器
console_handler = logging.StreamHandler()
# 设置 日志级别过滤器
console_handler.setLevel(logging.INFO)
# 设置 日志格式
console_handler.setFormatter(formatter)

# 添加日志处理器
logger.addHandler(get_wan_ip_file_handler)
# logger.addHandler(console_handler)



# 实例化logging
error_logger = logging.getLogger("error")
# 设置logger日志级别
error_logger.setLevel(level=logging.INFO)

# 实例化 文件轮询日志处理器
# 第三个参数是日志文件的最大容量,单位是byte,换算单位以后是100M
# 第四个参数是轮换的次数
error_file_handler = RotatingFileHandler(get_config("log", "error_log_data"),
                                   'a',
                                   int(get_config("log", "max_Bytes")),
                                   get_config("log", "backup_count")
                                   )
# 设置 日志级别过滤器
error_file_handler.setLevel(logging.INFO)
# 设置 日志格式
error_file_handler.setFormatter(formatter)

error_logger.addHandler(error_file_handler)