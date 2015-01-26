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

class ProducerThread(Thread):
        def run(self):
                global queue
                for x in c.url_select():
                        l = []
                        l.append(x)
                        l.append(m.check_url(x[2]))
                        queue.put(l)


class ConsumerThread(Thread):
        def run(self):
                global queue
                for x in c.url_select():
                        result = queue.get()
                        if result[1] == 0:
                                r.redis_modify(result[0][0])
                                continue
                        else:
                                if r.redis_select(result[0][0]) < 3:
                                        r.redis_insert(result[0][0])
                                else:
                                        print r.redis_select(result[0][0])
                                        for user in c.user_select(result[0][1]):
                                                content = ''' 接口出问题了。。。。
Group:  %s
 URL :  %s
检测失败超过3次,尽快检查以免影响服务。。  
''' %(result[0][1],result[0][2])
                                                m.send_mail('URL检测失败',user[0],content)
                                                r.redis_insert(result[0][0])
                queue.task_done()


#由于url数量较多，这里用到了多线程
ProducerThread().start()
ConsumerThread().start()