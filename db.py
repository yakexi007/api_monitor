#!/usr/bin/env  python
# -*- coding:utf-8 -*-

import redis
import MySQLdb

r = redis.Redis(host='127.0.0.1',port=6379)
conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='123',db='monitor_url',port=3306)
cur = conn.cursor()

class redis_count:

        def redis_select(self,id):
                result = r[id]
                return result
        def redis_insert(self,id):
                r[id] = int(r[id]) + 1
        def redis_modify(self,id):
                r[id] = 0

class mysql_select:
        def url_select(self):
                sql = "select * from url_info;"
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

        def user_select(self,gp):
                sql = "select email,phone from user_info where gp = '%s';" %gp
                cur.execute(sql)
                result = []
                for x in cur.fetchall():
                        result.append(x)
                return result

if __name__ == '__main__':
        print 'This is redis moudle...'