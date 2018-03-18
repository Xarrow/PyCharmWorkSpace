# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: helix
 Site: https://iliangqunru.bitcron.com/
 File: test_exector.py
 Time: 3/17/18
"""
import logging
import requests

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)

import concurrent.futures

url_list = [
    "https://www.baidu.com",
    "https://www.sina.com",
    "https://www.taobao.com",
    "https://tmall.com"
]


def requests_url(url: str) -> str:
    """请求"""
    resp = requests.get(url=url)
    if resp.status_code == 200:
        return resp.text
    return ""

#submit
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    for url in url_list:
        future = executor.submit(requests_url,url)
        print("--> %s " % future.result())
executor.shutdown(wait=True)
print("")


# Executor.map
# with concurrent.futures.ThreadPoolExecutor(max_workers=10) as exector:
#     for url, res in (exector.map(requests_url, url_list)):
#         print("%s <---> %s" % (url, res))
