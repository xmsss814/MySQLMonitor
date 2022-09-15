# MySQLMonitor
监控mysql执行sql语句的小工具，用于代码审计

## 环境 ：
python==3.8

## 库文件：
pandas
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
