#url_monitor
我是将mysql中url的id字段存放到redis中，根据id更新检测失败次数，检测次数存放在redis中，然后做出判断是否发送报警
数据库 url字段  id group url
数据库 user_info字段  id group mail phone 用于发送邮件和短信
由于各组的接口以及url返回值不统一，只能做不同的判断。