import os
import sys
dir=os.path.abspath('..')
sys.path.append(dir)
from utils.mysql_util.MysqlConn import MySql
from utils.logging.getLogger import GetLogger
if __name__ == '__main__':
    mysql = MySql()
    sql = "select * from user"
    logger = GetLogger(logs_dir='../../logs').get_logger()
    logger.info("执行了" + sql)
    result = mysql.getAll(sql)
    if result :
        print("get all")
        for row in result:
            print(type(row['id']))
    print('phone')
    result1 = mysql.getMany(sql, 2)
    if result1 :
       print(result1)
    mysql.end()
    mysql.dispose()
    print("")
