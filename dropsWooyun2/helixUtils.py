# -*- coding: utf-8 -*-
__title__ = 'helixUtils'
__author__ = 'zhangjian5'
__version__ = 'beta1.0'

import sys
import time

import ConfigParser

reload(sys)
sys.setdefaultencoding('utf-8')
"""
    完善日志记录
    参考:https://docs.python.org/2/howto/logging-cookbook.html
"""
import logging

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%yy-%m-%d %H:%M'
"""
    Does Python's time.time() return the local or UTC timestamp?
    http://stackoverflow.com/questions/13890935/does-pythons-time-time-return-the-local-or-utc-timestamp
"""
filename = str(time.time())
filemode = 'w'
logging.basicConfig(level=level, format=format, datefmt=datefmt, filename=filename, filemode=filemode)

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)
logger = logging.getLogger(__name__)

try:
    import requests
except ImportError:
    logger.warn("Can not find requests module")
    pass

# 读取配置文件
cf = ConfigParser.ConfigParser()


class Helix:
    def __init__(self):
        try:
            cf.read("config.ini")
        except:
            logger.warn("can not find config.ini")
        try:
            self.mainUrl = cf.get("configure", "mainUrl")  # 主连接
        except:
            logger.warn("can not read mainUrl")
        try:
            self.firstTag = cf.get("configure", "firstTag")  # 第一个条目
        except:
            logger.warn("can not read firstTag")

        self.session = requests.session()  # 保持同一个session

        self.targetPool = []  # 目标链接池
        self.errorPool = []  # 错误链接池
        self.cookies = ""

        self.headers_pc = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
        }  # pc端头信息
        self.headers_mo = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Linux; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.114 Mobile Safari/537.36"

        }  # 移动端头信息

        self.total_flag = 0
        self.error_flag = 0

    @staticmethod
    def setFistTag(firstTag):
        cf.set("configure", "firstTag", firstTag)
        cf.write(open('config.ini', 'wb'))

    def helloworld(self):
        """do nothing"""
