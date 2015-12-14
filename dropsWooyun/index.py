# -*- coding: utf-8 -*-
__author__ = 'Administrator'
"""
html2text bug:
    Long list lines do not wrap (长url包裹问题)
fix:
    change 'result += "\n".join(wrap(para, self.body_width))'
    to 'result += "".join(wrap(para, self.body_width))'
"""

from bs4 import BeautifulSoup
import html2text2
import sys
import os
import logging
import helixUtils
import time
reload(sys)
sys.setdefaultencoding("utf-8")


class WooYunArticle():
    def __init__(self):
        self.helix = helixUtils.Helix("http://drops.wooyun.org/")

    """
        遍历网页从中获取文章地址放入targetUrls[]中
        start page :http://drops.wooyun.org/page/1
        end page :http://drops.wooyun.org/page/88
    """

    def getTagetUrlsFromWebPages(self):
        logging.info("starting getTargetUrlsFromWebPages.")
        f = open(r'targetUrls.txt', 'wb')
        req = self.helix.session.get(url=self.helix.mainUrl)
        soup1 = BeautifulSoup(req.text)
        start = 1
        last = int(soup1.find('a', {'class': 'last'}).get('href').split('/')[-1])
        for i in xrange(start, last, 1):
            r = self.helix.session.get(url='http://drops.wooyun.org/page/index'.replace('index', str(i)))
            soup2 = BeautifulSoup(r.text)
            for i in soup2.find_all("a", {'rel': 'bookmark'}):
                self.helix.targetPool.append(i.get('href'))
                f.writelines(i.get('title').encode('utf-8') + ':' + i.get('href'))
                f.write('\r\n')
                logging.info('%s %s has been saved in targetUrls.txt' % (i.get('title'), i.get('href')))
        logging.info('一共抓取 :%d 条链接.' % len(self.helix.targetPool))
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
        i = self.helix.total_flag + 1
        j = self.helix.error_flag + 1
        logging.info('正在抓取文章喵..............')
        for url in self.helix.targetPool:
            r = self.helix.session.get(url=url, headers=self.helix.headers_pc)
            soup = BeautifulSoup(r.text.encode('utf-8'))
            title = soup.h1.string
            content = soup.article

            if not os.path.exists('markdownFile'):
                os.mkdir("markdownFile")
            try:
                f = open(r"markdownFile//" + title + ".md", 'w')
                f.write(str(html2text2.html2text(content.encode('utf-8'))))
                f.flush()
                f.close()
                logging.info('第%d条 %s : %s' % (i, title, url))
            except:
                self.helix.errorPool.append(url)
                logging.warn('第%d条 %s : %s 存在问题.' % (i, title, url))
                logging.info("正在处理异常 喵...........")
                updatedtitle = str(title).replace('/', '-').encode("utf-8")
                f = open(r'markdownFile//'+str(time.time())+'.txt', 'w')
                f.write(str(html2text2.html2text(content.encode('utf-8'))))
                f.flush()
                f.close()
                logging.info('第%d条 [%s -----> %s]'%(j, title,updatedtitle))
                j += 1
                pass
            i += 1

        logging.info('一共抓取 %d 篇文章,错误 %d ,错误率%s%%' % (i, j, format((float(j) / float(i)), '.2%')))
        logging.info("finish getArticles.")


# 主程序入口
def main():
    w = WooYunArticle()
    w.getTagetUrlsFromWebPages()
    w.getArticle()


if __name__ == '__main__':
    main()
