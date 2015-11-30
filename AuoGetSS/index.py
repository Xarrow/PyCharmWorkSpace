# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 13:19:43 2015

@author: zhangjian5
"""

import requests
import sys
import os
import time
import ConfigParser
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

class AutoGetGeneralSS():
    def __init__(self,main_url,data):
        self.main_url = main_url
        self.data = data
        self.session = requests.session()
        self.login_url = '/_login.php'
        self.node_url = '/node.php'
        self.targetUrls = [] 

    @staticmethod
    def loger(content):
         if not os.path.exists('logger'):
             os.mkdir('logger')
         f = open(r'logger//logger.txt','wb')
         f.write(content)
         f.write('\r\n')
         f.flush()
         f.close()
        
    def getTargetUrls(self):
        r = self.session.post(url=str(self.main_url+self.login_url),data=self.data)
        print self.main_url+self.login_url
        if r.status_code == 200:
            AutoGetGeneralSS.loger((time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) +":"+r.text))
            print '[+]loger:%s'%r.text
            ss_r = self.session.get(url=self.main_url+self.node_url)
            soup = BeautifulSoup(ss_r.text)
            nodeUrls = soup.find_all('a',{'role':'menuitem','target':'_blank'})
            for i in xrange(0,len(nodeUrls),2):
                self.targetUrls.append(self.main_url+nodeUrls[i].get('href'))
            print '[+]targetUrls has been finished.'
                
    def saveSS(self,localSSPath):
        f = open(localSSPath,'r')
        config = str(f.read())
        f.close()
        s = ''
        tmp = ''
        for j in self.targetUrls:
            AutoGetGeneralSS.loger(('[+]targetUrls is :%s'%j))
            print '[+]targetUrls is :%s'%j
            r = self.session.get(url=j)
            tmp+=r.text+','
            s = config[:config.index('[')+2]+tmp+config[config.index('[')+2:]
        print s        
        fw = open(localSSPath,'wb')
        fw.write(s)
        fw.close()
        
            
def main(config_file_path):
    cf = ConfigParser.ConfigParser()
    cf.read(config_file_path)
    
    main_url = cf.get('loginGeneralSS','mainUrl')
    userlists = cf.get('loginGeneralSS','userlists')
    localSSPath = cf.get('local','shadowscoksPath')

    users = userlists.split('|')
    for i in users:
        email = i.split('&')[0]
        passwd = i.split('&')[1]
        print email+':'+passwd
        data = dict(email=email, passwd=passwd,remember_me='week')
        a = AutoGetGeneralSS(main_url,data)
        a.getTargetUrls()
        a.saveSS(localSSPath)
if __name__=='__main__':
    main('config.ini')