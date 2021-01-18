import os
import sys
dir=os.path.abspath('..')
sys.path.append(dir)
from utils.mysql_util.MysqlConn import MySql

if __name__ == '__main__':
    mysql = MySql()
    time_list= ["2020-10-10 14:00:00", "2020-10-10 17:00:00"]
    #time_list = ["2020-10-10 13:00:00"]
    sql = "Delete from Mlmet where time_point = %s"
    result = 0
    for time_point in time_list:
        time_point =  [time_point]
        result += mysql.delete(sql, time_point)
    if result > 0:
        print(result)
    mysql.end()
    mysql.dispose()

