import sys
import os
dir=os.path.abspath('..')
sys.path.append(dir)
from utils.mysql_util.MysqlConn import MySql
from utils.logging.getLogger import GetLogger
import pandas as pd

#注意此时的路径
logger = GetLogger(logs_dir='./logs').get_logger()


class MlmetDB:
    def __init__(self):
        return
    def insertMany(self, value_list):
        mysql = MySql()
        sql = "INSERT INTO MLMET(TIME_POINT, POSITION_NAME, PRECIPITATION, TEMPERATURE, WS, WD, HUMIDITY, CLOUDRATE, SKYCON, PRESSURE, VISIBILITY, DSWRF, AQI, PM25)VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        logger.info("执行了" + sql)
        try:
            count = mysql.insertMany(sql, value_list)
            logger.info("批量插入成功！")
        except:
            logger.error("批量插入失败！")
            count = -1
        mysql.dispose()
        return count
    def insertUniqueMany(self, value_list):
        mysql = MySql()
        try:
            #删除上一个时刻爬取的重叠数据
            dt = value_list[0][0]
            dt = pd.to_datetime(dt)
            date_hour = str(dt.date()) + " " + str(dt.hour)
            begin_time = date_hour + ":00:00"
            end_time = date_hour + ":59:59"
            sql = "Delete from Mlmet where time_point >= %s and time_point <= %s"
            count = mysql.delete(sql,[begin_time, end_time])
            logger.info("执行了"+ sql +"操作，更新了" + str(count) + "条数据")
            #插入当前时刻的爬取的数据
            sql = "INSERT INTO MLMET(TIME_POINT, POSITION_NAME, PRECIPITATION, TEMPERATURE, WS, WD, HUMIDITY, CLOUDRATE, SKYCON, PRESSURE, VISIBILITY, DSWRF, AQI, PM25)VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            count = mysql.insertMany(sql, value_list)
            logger.info("执行了" + sql + " " + count + "条数据受到影响")
        except:
            logger.error("插入异常！")
            count = -1
        mysql.dispose()
        return count

    def deleteByTime(self, time_list):
        mysql = MySql()
        try:
            # 删除上一个时刻爬取的重叠数据
            sql = "Delete from Mlmet where time_point = %s"
            count = mysql.delete(sql, time_list)
            logger.info("执行了" + sql + "操作，更新了" + str(count) + "条数据")
        except:
            logger.error("插入异常！")
            count = -1
        mysql.dispose()
        return count