#!/usr/bin/env  python
# -*- coding:utf-8 -*-

import redis
import MySQLdb
import time

r = redis.Redis(host='10.10.10.10',port=6379)
conn = MySQLdb.connect(host='127.0.0.1',user='xxx',passwd='xxx',db='webserver',port=3306,charset="utf8")
cur = conn.cursor()

class redis_count:

        def redis_select(self,id):
                result = r[id]
                return int(result)
        def redis_insert(self,id):
                r[id] = int(r[id]) + 1
        def redis_modify(self,id):
                r[id] =  0

class mysql_select:
        def url_select(self):
                sql = "select * from monitor_urlmodel;"
                cur.execute(sql)
                result = []
                for x in cur.fetchall():
                        result.append(x)
                return result

        def port_select(self):
                sql = "select * from port_info;"
                cur.execute(sql)
                result = []
                for x in cur.fetchall():
                        result.append(x)
                return result

        def user_select(self,user):
                result = []
                for x in user.split(','):
                        sql = "select email,phone from url_userinfo where xm = '%s';" %x
                        cur.execute(sql)
                        info = cur.fetchall()
                        result.append(info[0])
                return result

        def update_time(self,id):
                t = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                sql = "update monitor_urlmodel set lasttime = '%s' where id = '%s';" %(t,id)
                cur.execute(sql)
                conn.commit()

if __name__ == '__main__':
        m = mysql_select()
        print m.user_select('api')
        print 'This is redis moudle...'