# -*- coding: utf-8 -*-
__author__ = 'Administrator'
"""
html2text bug:
    Long list lines do not wrap (长url包裹问题)
fix:
    change 'result += "\n".join(wrap(para, self.body_width))'
    to 'result += "".join(wrap(para, self.body_width))'
"""

import requests
from bs4 import BeautifulSoup
import html2text2
import sys
import os
import logging
import helixUtils

reload(sys)
sys.setdefaultencoding("utf-8")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WooYunArticle():
    def __init__(self):
        self.mainUrl = "http://drops.wooyun.org/"
        self.targetUrls = []
        self.errorUrls = []

    """
        遍历网页从中获取文章地址放入targetUrls[]中
        start page :http://drops.wooyun.org/page/1
        end page :http://drops.wooyun.org/page/88
    """

    def getTagetUrlsFromWebPages(self):
        logging.info("starting getTargetUrlsFromWebPages.")
        f = open(r'targetUrls.txt', 'wb')
        req = requests.get(url=self.mainUrl)
        soup1 = BeautifulSoup(req.text)
        start = 1
        last = int(soup1.find('a', {'class': 'last'}).get('href').split('/')[-1])
        for i in xrange(start, last, 1):
            r = requests.get(url='http://drops.wooyun.org/page/index'.replace('index', str(i)))
            soup2 = BeautifulSoup(r.text)
            for i in soup2.find_all("a", {'rel': 'bookmark'}):
                self.targetUrls.append(i.get('href'))
                f.writelines(i.get('title').encode('utf-8') + ':' + i.get('href'))
                f.write('\r\n')
                logging.info('%s %s has been saved in targetUrls.txt' % (i.get('title'), i.get('href')))
        logging.info('一共抓取 :%d 条链接.' % len(self.targetUrls))
        logging.info("finish getTargetUrlsFromWebPages.")

    """
        从网页中获取article区域的标题和文章，利用html2text2库，转为markdown格式
        get article html
    """

    def getArticle(self):
        log = open('log.txt', 'wb')
        t = ['http://drops.wooyun.org/papers/58',
             'http://drops.wooyun.org/papers/59',
             'http://drops.wooyun.org/tools/427',
             'http://drops.wooyun.org/papers/596',
             'http://drops.wooyun.org/papers/680',
             'http://drops.wooyun.org/tips/839',
             'http://drops.wooyun.org/papers/929'
             ]
        logging.info('正在抓取文章喵..............')
        i = 1
        for url in self.targetUrls:
            r = requests.get(url=url)
            soup = BeautifulSoup(r.text.encode('utf-8'))
            title = soup.h1.string
            content = soup.article

            if not os.path.exists('markdownFile'):
                os.mkdir("markdownFile")
            try:
                f = open("markdownFile//" + title + ".md", 'w')
                f.write(str(html2text2.html2text(content.encode('utf-8'))))
                f.flush()
                f.close()
                logging.info('第%d条 %s : %s' % (i, title, url))
            except:
                self.errorUrls.append(url)
                logging.warn('第%d条 %s : %s 存在问题.' % (i, title, url))
                pass
            i += 1
        logging.info('一共抓取 %d 篇文章,正确率%s%%' % (i, str(i / 1)))
        logging.info("finish getArticles.")


# 主程序入口
def main():
    w = WooYunArticle()
    w.getTagetUrlsFromWebPages()
    w.getArticle()


if __name__ == '__main__':
    main()
