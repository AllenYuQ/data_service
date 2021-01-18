import os
import sys
dir=os.path.abspath('../..')
sys.path.append(dir)
from utils.mysql_util.MysqlConn import MySql

if __name__ == '__main__':
    mysql = MySql()
    sql = "INSERT INTO Role (Role) VALUES(%s)"

    #必须获取id
    role1 = "test"
    role2 = "test1"
    result = mysql.insertMany(sql, [role1,role2])
    if result > 0:
        print(result)
    mysql.end()
    mysql.dispose()
    print("")
