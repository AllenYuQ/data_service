import os
import sys
dir=os.path.abspath('..')
sys.path.append(dir)
from utils.mysql_util.MysqlConn import MySql
from utils.logging.getLogger import GetLogger
if __name__ == '__main__':
    mysql = MySql()
    # list_values = [['test1'],['test2']]
    # logger = GetLogger(logs_dir='../../logs').get_logger()
    # sql = "INSERT INTO Role (Role) VALUES(%s)"
    # logger.info("执行了" + sql)
    list_values = [[6, 'pythontest3', 'pythontest2', 'pythontest2', '2969141711@qq.com', '18817239323', 1, 1],
                   [7, 'pythontest2', 'pythontest2', 'pythontest2', '2969141711@qq.com', '18817239322', 1, 1]]
    sql = "INSERT INTO USER(ID, USERNAME, REALNAME, PASSWD, EMAIL, PHONE, SEX, ROLE_ID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    result = mysql.insertMany(sql, list_values)
    if result :
       print(result)
    mysql.end()
    mysql.dispose()
    print("")
