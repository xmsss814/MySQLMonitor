import keyboard,pymysql,time,threading,click,sys
from colorama import init, Fore, Back, Style

REFRESH_TIME=1  #刷新时间 float 单位 s
EX=True  #是否持续查询
GENERAL_LOG = []   #存放sql执行语句的列表
NOTES_TAG = "  /*this python*/"    #标识为该脚本执行的sql语句
MAX_SIZE = 100 #最大一次读取sql记录条数
FILEPATH = "./MonitorLog/"  #存放日志文件的位置(csv)

"""
持续查询general_log
"""
def QurayRecording(cursor):
    global EX, GENERAL_LOG
    start=0
    init(autoreset=True)
    while(EX):
        time.sleep(REFRESH_TIME)
        cursor.execute("select * from mysql.general_log limit "+str(start)+","+str(MAX_SIZE)+NOTES_TAG)
        tuple = cursor.fetchall()
        start += len(tuple)
        for var in tuple:
            if NOTES_TAG in str(var[-1]): continue  #不存储和显示与该脚本查询语句相关的语句
            GENERAL_LOG.append(list(var))
            print(Fore.YELLOW+var[0].strftime('%H:%M:%S %f'),end="|")
            print(Fore.BLUE+f'{var[1]:>29}',end="|")
            print(Fore.RED+f'{var[4]:>8}', end="|")
            print(Fore.GREEN+str(var[-1],'utf-8'))
    print(Style.RESET_ALL)
    print("****************************停止监听sql****************************")

"""
监控键盘输入q，用于决定是否监听
"""
def MonitorStop():
    global EX
    keyboard.wait('q')
    EX=False
    print("——————开始收尾工作——————清理general_log表与存储文件等————会显示未显示完成的sql语句——————")

"""
主函数，用于代开关闭sql连接，以及存储
"""
@click.command()
@click.option("--host",help='主机ip')
@click.option("--username",default='root',help='数据库账号，非必选，默认root')
@click.option("--password",help='数据库密码，明文，暂时没做加密传输')
@click.option("--refresh",default=1,help='数据查询刷新时间，默认1秒')
def main(host,username,password,refresh):
    global REFRESH_TIME
    try:
        db = pymysql.connect(
            host=host,
            port=3306,
            user=username,
            passwd=password,
            database='mysql',
            charset='utf8'
        )
        cursor = db.cursor()
    except:
        print("连接信息错误，请重新输入")
        sys.exit(1)
    REFRESH_TIME=refresh
    cursor.execute("set global general_log = ON") #开启日志
    cursor.execute("set global log_output='table'") #将日志存储到general_log表中
    keyMonitor = threading.Thread(target=MonitorStop,name="key")
    sqlMonitor = threading.Thread(target=QurayRecording,name="sql",args=(cursor,))
    sqlMonitor.start()
    keyMonitor.start()
    sqlMonitor.join()
    cursor.execute("set global general_log = ON")
    cursor.execute("truncate table mysql.general_log")
    cursor.execute("set global log_output='file'")
    cursor.close()
    print("————————————————————————————已将sql语句全部打印————————————————————————————")
    temporary = time.strftime("%Y-%m-%d_%H~%M~%S",time.localtime())
    global FILEPATH
    FILEPATH=FILEPATH+temporary+".csv"
    with open(FILEPATH,"w") as file:
        it = iter(GENERAL_LOG)
        while True:
            try:
                for var in next(it):
                    file.write(str(var))
                    file.write(",")
                file.write("\n")
            except StopIteration:
                break
        file.close()


if __name__ == '__main__':
    print("                                                                                                    ")
    print("                                                                                                    ")
    print("          ##     ##        ####   ###   ###    ##     ##               #                            ")
    print("           ##   ##        #   #  #   #   #      ##   ##                    #                        ")
    print("           ##   ##  ## ## ##    #     #  #      ##   ##   ###  ####   ##  ###   ###  ## #           ")
    print("           # # # #   # #   ###  #     #  #      # # # #  #   #  #  #   #   #   #   #  ##            ")
    print("           # # # #   # #     ## #     #  #      # # # #  #   #  #  #   #   #   #   #  #             ")
    print("           #  #  #    #   #   #  #   #   #  #   #  #  #  #   #  #  #   #   #   #   #  #             ")
    print("          ### # ###   #   ####    ###   #####  ### # ###  ###  ### ## ###   ##  ###  ###            ")
    print("                    # #            #                                                                ")
    print("                    ##              ##                                                              ")
    print("                                                                                                    ")
    print("                                                                                                    ")
    print("MysqlMonitor————————————程序正常运行中，输入'q'结束程序————————————————by.sshui————————————version1.0")
    main()
    print("监控日志文件存放路径为："+FILEPATH)
    print("欢迎使用sshui开发的小工具MySQLMonitor~")

