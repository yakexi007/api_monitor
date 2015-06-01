#!/usr/bin/env  python
# -*- coding: utf-8 -*-

import time
import pycurl
import urllib2
import urllib
import sys
import StringIO
import smtplib  
import socket
import json
import hashlib
from email.mime.text import MIMEText 
#reload(sys)
#sys.setdefaultencoding('utf-8')

class Monitor:
    def check_url(self,url):
		if url[6] != '':
			send_headers = eval("{%s}" %url[6].encode('utf8'))
		else:
			send_headers = {}
			request = urllib2.Request(url[3],headers=send_headers)
		try:
			#print url[3]
			response = urllib2.urlopen(request,timeout=5)
			return_data = response.read()
			http_code = response.getcode()
			if url[7] != '':
            	if return_data.find(url[7]) > 0:
                    return 0
                else:
                    return 1
        	else:
        		if http_code == 200:
                	return 0
            	else:
                	return 2
			
		except urllib2.URLError,e:
	        return 3

	def check_port(self,x):
        try:
            sc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            #设置超时时间（0.0）
            sc.settimeout(2)
            sc.connect((x[0],x[1]))
            sc.close()
            return 0
        except:
            return 1

    def send_mail(self,sub,user,content):
        msg = MIMEText(content,_subtype = 'plain',_charset = 'gb2312')  
        msg['Subject'] = sub  
        msg['From'] = 'tv-v-no@zabbix.com'
        msg['To'] = user
        try:  
            server = smtplib.SMTP()  
            server.connect('localhost')  
            server.sendmail('tv-v-no@zabbix.com', user, msg.as_string())  
            server.close()  
        except Exception, e:  
            return False

    def send_sms(self,phone,content):
        times = time.strftime("%Y%m%d%H%M%S", time.localtime())
        appid = "xxxxxxx"
        key = "xxxxxxxxxxx" #验证key
        priority = 3
        m = hashlib.md5()
        m.update(appid + str(phone) + content + times + key)  #enc验证 需要appid 手机
        md5 = m.hexdigest().encode('utf-8')           #将enc验证编码改为utf-8
        content1 = urllib.quote(content.encode('utf-8','replace'))  #将中文内容改为url编码

        URL = "http://xxxxxxxx/WLS/smsaccess/mt?appid=100190&destnumber=%s&content=%s&enc=%s&timestamp=%s&linkid=0&priority=3&tailsp=" %(str(phone),content1,md5,times)
        c = pycurl.Curl()
        b = StringIO.StringIO()
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        c.setopt(c.URL, URL)
        c.setopt(pycurl.TIMEOUT, 5)
        c.setopt(pycurl.NOPROGRESS, 1)
        c.setopt(pycurl.FORBID_REUSE, 1)
        c.setopt(pycurl.DNS_CACHE_TIMEOUT, 30)

        try:
            c.perform()
            html=b.getvalue()
            print html
        except Exception,e:
            c.close()
if __name__ == "__main__":
    print "This is a moudel..."
