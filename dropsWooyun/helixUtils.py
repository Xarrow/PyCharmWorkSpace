# -*- coding: utf-8 -*-
__title__ = 'helixUtils'
__author__ = 'zhangjian5'
__version__ = 'beta1.0'

import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')

import logging

logging.basicConfig(filename="log.md", level=logging.INFO)
logger = logging.getLogger(__name__)
logger = logging
try:
    import requests
except ImportError:
    logger.warn("Can not find requests module")
    pass


class Helix:
    def __init__(self, mainUrl):
        self.mainUrl = mainUrl  # 主连接
        self.session = requests.session()  # 保持同一个session
        self.targetPool = []  # 目标链接池
        self.errorPool = []  # 错误链接池

        self.headers_pc = {

        }  # pc端头信息
        self.headers_mo = {

        }  # 移动端头信息

    @staticmethod
    def hello():
        logger.info("hello")


if __name__ == '__main__':
    logging.info("hekmasd")
