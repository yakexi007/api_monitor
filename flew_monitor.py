#!/usr/bin/env  python
import time
import redis
import MySQLdb

r = redis.Redis(host='10.16.48.81',port=6379)
conn = MySQLdb.connect(host='10.16.48.81',user='root',passwd='123',db='weblog',port=3306)
cur = conn.cursor()

def NetInfo(dev):
    netdev = file('/proc/net/dev')
    netInfo = netdev.readlines()
    netdev.close()
    for line in netInfo:
        if line.lstrip().startswith(dev):
            line = line.replace(':', ' ')
            items = line.split()
            netin0 = long(items[1])
            netout0 = long(items[len(items)/2 + 1])

    return netin0,netout0


def net(dev):
    net_list = []

    netin0,netout0 = NetInfo(dev)
    time.sleep(0.995)
    netin1,netout1 = NetInfo(dev)
    netin = netin1 - netin0
    netin = int(netin / 1024 /1024)

    netout = netout1 - netout0
    netout = int(netout / 1024 /1204)

    net_list.append(netin)
    net_list.append(netout)
    return net_list

while 1:
        data = net('bond0') #需要监控的网卡名
        #结果写入数据库
        sql = "insert into logweb_flow_info (nginx_date,nginx_ip,nginx_in,nginx_out) values ('%s','%s','%s','%s')" %(time.strftime('%y%m%d%H%M%S'),'10.10.22.113',data[0],data[1])
        cur.execute(sql)
        conn.commit()
        list = eval(r['flow_113']) #同时存入redis 用于页面数据展示
        if len(list) < 19:
                list.append(data)
                r['flow_113'] = list
        else:
                list.pop(0)
                list.append(data)
                r['flow_113'] = list
        time.sleep(10)