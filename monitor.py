#!/usr/bin/env  python
# -*- coding: utf-8 -*-

import time
from db import *
from check_moudel import *
import time,random
from threading import Thread,Condition
from Queue import Queue

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
                        l.append(m.check_url(x[2]))
                        queue.put(l)


class ConsumerThread(Thread):
        def run(self):
                for x in a:
                        result = queue.get()
                        print result
                        if result[1] == 0:
                                r.redis_modify(result[0][0])
                                continue
                        else:
                                if r.redis_select('%s' %result[0][0]) < 3:
                                        r.redis_insert(result[0][0])
                                else:
                                        for user in c.user_select(result[0][1]):
                                                content = ''' 接口出问题了。。。。
Group:  %s
 URL :  %s
检测失败超过3次,尽快检查以免影响服务。。  
''' %(result[0][1],result[0][2])
                                                m.send_mail('URL检测失败',user[0],content)
                                        r.redis_insert(result[0][0])
#                       queue.task_done()


ProducerThread().start()
#time.sleep(1)
ConsumerThread().start()