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
        self.helix = helixUtils.Helix()

    """
        遍历网页从中获取文章地址放入targetUrls[]中
        start page :http://drops.wooyun.org/page/1
        end page :http://drops.wooyun.org/page/88
    """

    def getTagetUrlsFromWebPages(self):
        logging.info("starting getTargetUrlsFromWebPages.")
        # 获取乌云知识库首页内容
        req = self.helix.session.get(url=self.helix.mainUrl, headers=self.helix.headers_pc)
        # 用beautifulsoup解析
        soup1 = BeautifulSoup(req.text)
        # start为第一页
        start = 1
        # 解析获取最后一页
        last = int(soup1.find('a', {'class': 'last'}).get('href').split('/')[-1])
        for i in xrange(start, last, 1):
            # 循环获取每一页上内容
            r = self.helix.session.get(url='http://drops.wooyun.org/page/' + str(i))
            soup2 = BeautifulSoup(r.text)
            # 从配置文件中读取第一条文章的链接
            firstNo = self.helix.firstTag.split('/')[-1]
            # 使用beautifulsoup解析出文章的连接
            for i in soup2.find_all("a", {'rel': 'bookmark'}):
                # 判断firstTag 是否在第一条，如果不在就继续抓取，如果在则说明已经抓取过
                if firstNo not in  i.get('href'):
                    # 将目标链接放入 targetPool List当中
                    self.helix.targetPool.append(i.get('href'))
                    # 日志记录链接已经写入文件
                    logging.info('%s %s has been saved in targetUrls.txt' % (i.get('title'), i.get('href')))
                else:
                    try:
                        self.helix.setFistTag(self.helix.targetPool[0])
                        logging.info("链接已经存在.")
                    except:
                        logging.info("链接已经存在.")
                    finally:
                        return
        self.helix.setFistTag(self.helix.targetPool[0])
        logging.info('一共抓取 :%d 条链接.' % len(self.helix.targetPool))
        logging.info("finish getTargetUrlsFromWebPages.")

    """
        从网页中获取article区域的标题和文章，利用html2text2库，转为markdown格式
        get article html
    """

    def getArticle(self):
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
                f = open(r'markdownFile//' + str(time.time()) + '.md', 'w')
                f.write(str(html2text2.html2text(content.encode('utf-8'))))
                f.flush()
                f.close()
                logging.info('第%d条 [%s -----> %s]' % (j, title, updatedtitle))
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
