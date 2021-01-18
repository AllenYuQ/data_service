import sys
import os
dir=os.path.abspath('..')
sys.path.append(dir)
import MySQLdb
con = MySQLdb.connect("124.71.156.219:61198", "root", "Lc202010Iotgateway", "air", charset="utf8")
#静态代码块，后期修改
class DBMlmet:
    def __int__(self):
        """
        :param db:传入操作数据库的实例
        :return:
        """
        return
    #以后改成批量
    def insert(self, time_point, position_name, precipitation, temperature, ws, wd, humidity, cloudrate, skycon, pressure, visibility, dswrf, aqi, pm25):
        cursor = con.cursor()
        sql = "INSERT INTO MLMET(TIME_POINT, POSITION_NAME, PRECIPITATION, TEMPERATURE, WS, WD, HUMIDITY, CLOUDRATE, SKYCON, PRESSURE, VISIBILITY, DSWRF, AQI, PM25)VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
              "'%s', '%s')" % \
              (time_point, position_name, precipitation, temperature, ws, wd, humidity, cloudrate, skycon, pressure,visibility, dswrf, aqi, pm25)
        print(sql)
        try:
            cursor.execute(sql)
            cursor.close()
            con.commit()
        except:
            print('出现错误，回滚')
            cursor.close()
            con.rollback()
    def select(self):
        cursor = con.cursor()
        sql = "select * from user"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                userName = row[1]
                password = row[2]
                print(userName + ":" + password)
            cursor.close()
        except:
            print("出现了错误!")
            cursor.close()
            con.rollback()
    def release_con(self):
        con.close()
