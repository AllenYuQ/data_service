import os
import sys
dir=os.path.abspath('..')
sys.path.append(dir)
from utils.mysql_util.MysqlConn import MySql
if __name__ == '__main__':
    mysql = MySql()
    sql = "select * from mlout "
    result = mysql.getAll(sql)
    if result :
        #print("get all")
        print(result)
    mysql.dispose()
    print("")
