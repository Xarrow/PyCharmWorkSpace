# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: helix
 Site: https://iliangqunru.bitcron.com/
 File: weibo_crawl.py
 Time: 3/16/18
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

import datetime

now = datetime.datetime.now()
CURRENT_TIME = now.strftime('%Y-%m-%d %H:%M:%S')
CURRENT_YEAR = now.strftime('%Y')
CURRENT_YEAR_WITH_DATE = now.strftime('%Y-%m-%d')


def get_weibo(container_id='1076033788713745', page=25):
    api = "https://m.weibo.cn/api/container/getIndex"

    def gen_result(page):
        """解析微博内容"""

        while page > 0:
            params = {"containerid": container_id, "page": page}

            _response_json = requests.get(url=api, params=params).json()
            logger.info("核心解析==> %s" % _response_json)

            item_list = []
            containerid = _response_json.get("data").get("cardlistInfo").get("containerid")
            cards = _response_json.get('data').get("cards")
            for _cards in cards:
                # 结束推荐
                if _cards.get("card_group"):
                    continue
                itemid = _cards.get("itemid")
                scheme = _cards.get("scheme")

                created_at = _cards.get('mblog').get("created_at")
                if len(created_at) < 9 and str(created_at).__contains__("-"):
                    created_at = CURRENT_YEAR + "-" + created_at
                if not str(created_at).__contains__("-"):
                    created_at = CURRENT_YEAR_WITH_DATE
                mid = _cards.get('mblog').get("mid")
                text = _cards.get('mblog').get("text")
                source = _cards.get('mblog').get("source")
                userid = _cards.get('mblog').get("user").get("id")
                reposts_count = _cards.get('mblog').get("reposts_count")
                comments_count = _cards.get('mblog').get("comments_count")
                attitudes_count = _cards.get('mblog').get("attitudes_count")
                raw_text = ""
                if _cards.get('mblog').get("raw_text"):
                    raw_text = _cards.get('mblog').get("raw_text")
                bid = _cards.get('mblog').get("bid")

                pics_dict = {}
                if _cards.get('mblog').get("pics"):
                    pics = str(_cards.get('mblog').get("pics"))
                    pics_dict['weibo_pics'] = pics

                mblog = str(_cards.get('mblog'))

                yield mblog
            page += -1

    yield from gen_result(page)


if __name__ == '__main__':
    for tweet in get_weibo():
        print(tweet)
