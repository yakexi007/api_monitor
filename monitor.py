#!/usr/bin/env  python
# -*- coding: utf-8 -*-

import time
from db import *
from check_moudel import *
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
                        print result
                        if result[1] == 0:
                                r.redis_modify(result[0][0])
                                continue
                        else:
                                if r.redis_select(result[0][0]) < 3:
                                        r.redis_insert(result[0][0])
                                else:
                                        if result[0][4] == 'on':
                                                for user in c.user_select(result[0][8]):
                                                        content = '''Group:  %s   URL :  %s  检测失败''' %(result[0][2],result[0][3])
                                                        m.send_mail('URL检测失败',user[0],content)
                                                        m.send_sms(user[1],content)
                                                        #m.send_sms('18610941029',content)
                                                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                                with open('sms.txt','a+') as f:
                                                        f.write(times + '\n')
                                                        f.write(content + '\n' + '\n')
                                                c.update_time(result[0][0])
                                                r.redis_insert(result[0][0])
                                        else:
                                                r.redis_insert(result[0][0])
                                                continue
#                       queue.task_done()


ProducerThread().start()
#time.sleep(1)
ConsumerThread().start()
You have mail in /var/spool/mail/root