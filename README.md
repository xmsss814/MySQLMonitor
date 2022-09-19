# MySQLMonitor
监控mysql执行sql语句的小工具，用于代码审计

## 环境 ：
python==3.8

## 库文件：
colorama
keyboard
pymysql
threading
click
sys
time

## 原理：
设置mysql打开general_log记录日志，同时设置日志存储到general_log表中。
然后对mysql.general_log表进行读取，从而获取sql语句执行记录

## 使用教程：
python main.py --host 主机ip --username 数据库用户名，默认root --password 数据库密码 --refresh 数据查询的刷新时间，默认1（单位：秒）
当程序正常运行过程中，按‘q’结束程序运行

## 其他：
程序会将监听到的sql语句存储到 ./MonitorLog/****.csv 文件
