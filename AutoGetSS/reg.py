# -*- coding: utf-8 -*-
__author__ = 'Jian'
import requests
from bs4 import BeautifulSoup
import sys
import os
import time
from subprocess import Popen
import webbrowser
import logging
import ConfigParser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
reload(sys)
sys.setdefaultencoding('utf-8')

'''http://user.jumpss.com/user/register.php'''


class RegSS():
    def __init__(self, main_url, nick, email, passwd):
        self.main_url = main_url
        self.name = nick
        self.email = email
        self.passwd = passwd
        self.keys = ''
        self.reg = '/_reg.php'
        self.session = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
            'Host': 'user.jumpss.com',
            'Origin': 'http://user.jumpss.com',
            'Connection': 'keep-alive',
            'Referer': 'http://user.jumpss.com/user/register.php',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'
        }

    def getCaptcha(self):
        logging.info("Start get captcha ")

        timsstamp = str(int(time.time() * 1000))
        captcha_URL = 'http://user.jumpss.com/authnum.php?1'
        print captcha_URL
        captcha = self.session.get(url=captcha_URL, headers=self.headers)
        if not os.path.exists("captcha"):
            os.mkdir("captcha")
        # save captcha
        # @sys.path[0]
        try:
            with open("captcha\\" + timsstamp + '.png', 'wb') as f:
                f.write(captcha.content)
            Popen(sys.path[0] + "\\captcha\\" + timsstamp + '.png', shell=True)
        except:
            raise '[!]Captha get failed,error from method of getCaptcha().'
        self.keys = str(raw_input("[+]input captcha:"))
        logging.info("[+]The captcha is :%s", self.keys)

    def reg1(self):
        logging.info("Start register a new user")
        r2 = self.session.post(url=(self.main_url + self.reg),
                               data=dict(email=self.email, name=self.name, passwd=self.passwd, repasswd=self.passwd,
                                         code='', keys=self.keys, invitee='')
                               )
        if 'ok' in str(r2.text):
            logging.info("register success")
            logging.info('register email:%s , passwd:%s' % (self.email, self.passwd))
        else:
            logging.info('[!]register failed.')

        # unicode 转中文参考 http://windkeepblow.blog.163.com/blog/static/1914883312013988185783/
        logging.info("register info:%s", r2.text.decode("unicode_escape"))
        logging.info("register finished")


def main(config_file_path):
    cf = ConfigParser.ConfigParser()
    cf.read(config_file_path)
    #写入配置文件
    # cf.add_section("TestConfigParser")
    # rawUserLists = cf.get("loginGeneralSS","userlists")
    # cf.set("loginGeneralSS","userlists", rawUserLists+'|Test1&test1')
    # cf.write(open("config.ini","wb"))
    mainUrl = cf.get("registerInfo", "mainUrl")
    nick = cf.get("registerInfo", "nick")
    passwd = cf.get("registerInfo", "passwd")
    email = cf.get("registerInfo", "email")
    r = RegSS(mainUrl, nick, email, passwd)
    r.getCaptcha()
    r.reg1()

###################Test##########################
if __name__ == '__main__':
    main('config.ini')
