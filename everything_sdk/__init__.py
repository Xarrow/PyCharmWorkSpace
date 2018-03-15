# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: zhangjian
 Site: http://iliangqunru.com
 File: 
 Time: 2018/3/9
"""
import logging

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)
PY3 = False

if sys.version > '3':
    PY3 = True