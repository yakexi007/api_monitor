#!/usr/bin/env  python
# -*- coding: utf-8 -*-

import time
from db import *
from check_moudel import *
from send import *
import time,random
from threading import Thread,Condition
from Queue import Queue
reload(sys)
sys.setdefaultencoding('utf-8')

m = Monitor()
r = redis_count()
c = mysql_select()
queue = Queue()
a = c.url_select()

class ProducerThread(Thread):
    def run(self):
        global queue
        for x in a:
            l = []
            l.append(x)
            l.append(m.check_url(x))
            queue.put(l)

class ConsumerThread(Thread):
    def run(self):
        global queue
        for x in a:
            result = queue.get()
            user = c.user_select(result[0][8])
            if result[0][4] != 'Yes':continue
            if result[1] == 0:
                if r.redis_select(result[0][0]) == 0:continue
                if r.redis_select(result[0][0]) < 3:
                    r.redis_modify(result[0][0])
                    with open('/data/scripts/monitor/sms.txt','a+') as f:
                        f.write('%s\t%s\t%s\n' %(result[0][1],result[0][2],result[0][3]))
                    c.insert_log(result)
                else:
		    content = '''Group:  %s   URL :  %s  恢复正常''' %(result[0][2],result[0][3])
                    title = 'URL恢复正常'
                    send(title,content,user)
                    r.redis_modify(result[0][0])
            elif result[1] != 0:
                if r.redis_select(result[0][0]) < 3:
                    r.redis_insert(result[0][0])
                else:
                    title = 'URL检测失败'
                    if result[1] == 1:
                        content = '''Group:  %s   URL :  %s  关键字检测失败!!!''' %(result[0][2],result[0][3])
                        send(title,content,user)
                        c.update_time(result[0][0])
                        r.redis_insert(result[0][0])
                    elif result[1] == 2:
                        content = '''Group:  %s   URL :  %s  返回状态码错误!!!''' %(result[0][2],result[0][3])
                        send(title,content,user)
                        c.update_time(result[0][0])
                        r.redis_insert(result[0][0])
                    elif result[1] == 3:
                        content = '''Group:  %s   URL :  %s  超5s 没有返回数据!!!''' %(result[0][2],result[0][3])
                        send(title,content,user)
                        c.update_time(result[0][0])
                        r.redis_insert(result[0][0])

ProducerThread().start()
ConsumerThread().start()
