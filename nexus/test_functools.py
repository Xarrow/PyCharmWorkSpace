# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: helix
 Site: https://iliangqunru.bitcron.com/
 File: test_functools.py
 Time: 3/13/18
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

from functools import cmp_to_key

a = sorted([1,465,77,9,0,345,78],key=cmp_to_key(lambda x,y:x-y))
print(a)

from functools import lru_cache

# key function

student_tuple_list = [
    ('zhang','A',10),
    ('liang','H',10),
    ('chang','A',12)
]

s_sort = sorted(student_tuple_list,key=lambda student:student[1],reverse=True)
print(s_sort)

