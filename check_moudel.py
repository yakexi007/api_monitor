#!/usr/bin/env  python
# -*- coding: utf-8 -*-

import time
import pycurl
import StringIO
import smtplib  
import socket
import json
from email.mime.text import MIMEText 
#reload(sys)
#sys.setdefaultencoding('utf-8')

class Monitor:
        def check_url(self,url):
                c = pycurl.Curl()
                b = StringIO.StringIO()
                c.setopt(pycurl.WRITEFUNCTION, b.write)
                c.setopt(c.URL, url)
                c.setopt(pycurl.CONNECTTIMEOUT, 20) 
                c.setopt(pycurl.TIMEOUT, 20) 
                #c.setopt(pycurl.NOPROGRESS, 1) 
                #c.setopt(pycurl.FORBID_REUSE, 1)
                #c.setopt(pycurl.MAXREDIRS, 1)
                c.setopt(pycurl.DNS_CACHE_TIMEOUT, 30)

                try:
                        c.perform()
                        http_code = c.getinfo(pycurl.HTTP_CODE)
                        html=json.loads(b.getvalue())
                        if isinstance(html,list):
                                if http_code == 200:
                                        return 0
                                else:
                                        return 1
                        elif isinstance(html,dict):
                                if http_code == 200 and "status" in html.keys() and html["status"] == 200: #api mvms组监控条件
                                        return 0
                                elif http_code == 200 and "response" in html.keys() and html["response"]["numFound"] > 0: #search组
                                        print "search"
                                        return 0
                                elif http_code == 200: #不根据返回值字段的监控
                                        return 0
                                else:
                                        return 1
                        else:
                                return 1
                        c.close()
                except Exception, e:
                        http_code = c.getinfo(pycurl.HTTP_CODE)
                        if http_code == 200:  #返回值不是json串的监控
                                return 0
                        elif http_code != 200:
                                return 1
                        else:
                                print "connection error:" + str(e)
                        c.close()

        def check_port(self,ip,port):
                try:
                        sc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                        #设置超时时间（0.0）
                        sc.settimeout(2)
                        sc.connect((ip,port))
                        sc.close()
                        return 0
                except:
                        timenow=time.localtime()
                        datenow = time.strftime('%Y-%m-%d %H:%M:%S', timenow)
                        logstr="%s:%s 端口连接失败->%s \n" %(ip,port,datenow)
                        return logstr

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

if __name__ == "__main__":
        print "This is a moudel..."