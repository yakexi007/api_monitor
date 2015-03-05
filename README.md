#url_monitor

将mysql中url的id字段存放到redis中，根据id更新检测失败次数，检测次数存放在redis中，然后做出判断是否发送报警

数据库 url字段  id 描述 部门  url  报警开关  上次报警时间  header  检测关键字  报警接收人（报警接收人格式为 张三，李四，王五）

数据库 user_info字段  id 报警接收人 邮件 电话  用于发送邮件和短信