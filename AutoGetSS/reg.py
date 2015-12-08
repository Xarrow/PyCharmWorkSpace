# -*- coding: utf-8 -*-
__author__ = 'Jian'
import requests
from bs4 import  BeautifulSoup
import sys
import os
import time
from subprocess import Popen
import webbrowser

reload(sys)
sys.setdefaultencoding('utf-8')

'''http://user.jumpss.com/user/register.php'''
class RegSS():
    def __init__(self,main_url,nick,email,passwd):
        self.main_url = main_url
        self.name= nick
        self.email = email
        self.passwd= passwd
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
        timsstamp = str(int(time.time() * 1000))
        captcha_URL = 'http://user.jumpss.com/authnum.php?1'
        print captcha_URL
        captcha = self.session.get(url=captcha_URL, headers=self.headers)
        if not os.path.exists("captcha"):
            os.mkdir("captcha")
        # save captcha
        #@sys.path[0]
        try:
            with open("captcha\\" + timsstamp + '.png', 'wb') as f:
                f.write(captcha.content)
            Popen(sys.path[0] + "\\captcha\\" + timsstamp + '.png', shell=True)
        except:
            raise '[!]Captha get failed,error from method of getCaptcha().'
        self.keys = str(raw_input("[+]input captcha:"))

    def reg1(self):

        r= self.session.post(url=(self.main_url+self.reg),
                             data=dict(email=self.email,name=self.name,passwd=self.passwd,repasswd=self.passwd,code='',keys=self.keys,invitee='')
                             )
        print self.main_url+self.reg
        print self.keys
        print r.text


if __name__=='__main__':
    main_url = 'http://user.jumpss.com/user'
    '''昵称(中文至少两个，英文与数字至少五位)
        密码(至少7位数'''
    r = RegSS(main_url,'张三','rewrfsefa@gmail.com','aaaaaaaa')
    r.getCaptcha()
    r.reg1()