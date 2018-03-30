# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: helix
 Site: https://iliangqunru.bitcron.com/
 File: nexus_sample.py
 Time: 3/7/18
"""
import logging
import sys
import os
import requests

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)
import contextlib2

@contextlib2.contextmanager
def file_save(file_name:str)->None:
    f = open(file_name,'w')
    yield f
    f.close()

with file_save('test_file') as f:
    f.write('test_data')
