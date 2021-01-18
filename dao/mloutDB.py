import sys
import os
dir=os.path.abspath('..')
sys.path.append(dir)
from utils.mysql_util.MysqlConn import MySql
from utils.logging.getLogger import GetLogger
#注意此时的路径
logger = GetLogger(logs_dir='./logs').get_logger()

class MloutDB:
    def __init__(self):
        return

    def insertMany(self, value_list):
        mysql = MySql()
        sql = "INSERT INTO MLOUT(time_point, station_name, substance, prediction_value)VALUES(%s, %s, %s, %s)"
        logger.info("执行了" + sql)
        try:
            count = mysql.insertMany(sql, value_list)
            logger.info("批量插入成功！")
        except:
            logger.error("批量插入失败！")
            count = -1
        mysql.dispose()
        return count

    #删除之前的数据
    def deleteByTimePoint(self, time_list):
        mysql = MySql()
        sql = "delete from Mlout where time_point = %s"
        logger.info("执行了" + sql)
        try:
            count = 0
            for time_point in time_list:
                time_point = [time_point]
                count += mysql.delete(sql, time_point)
            logger.info("删除成功!" + str(count) + "条数据受到了影响")
        except:
            logger.info("删除失败")
            count = -1
        mysql.dispose()
        return count

    #删除之前预测的数据
    def deleteMany(self, begin_time, end_time):
        mysql = MySql()
        sql = "delete from Mlout where time_point >= %s and time_point <= %s"
        logger.info("执行了" + sql)
        try:
            count = mysql.delete(sql, [begin_time, end_time])
            logger.info("删除成功!" + str(count) + "条数据受到了影响")
        except:
            logger.info("删除失败!")
            count = -1
        mysql.dispose()
        return count


