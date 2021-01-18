import sys
import os
dir=os.path.abspath('..')
sys.path.append(dir)
class Mlmet:
    def __init__(self):
        self.positionName = ""
        self.cloudrate = 0.0
        self.dswrf = 0.0
        self.humidity = 0.0
        self.precipitation = 0.0
        self.pressure = 0.0
        self.skycon = 0.0
        self.temperature = 0.0
        self.visibility = 0.0
        self.wd = 0.0
        self.ws = 0.0
        self.pm25 = 0.0
        self.aqi = 0.0
    def print_info(self):
        dic = {'positionName:':self.positionName,'cloudrate': self.cloudrate, 'dswrf': self.dswrf, 'humidity': self.humidity, 'precipitation': self.precipitation,
               'pressure': self.pressure,'skycon':self.skycon, 'temperature':self.temperature, 'visibility':self.visibility, 'wd':self.wd
               ,'ws':self.ws, 'pm25':self.pm25, 'aqi':self.aqi}
        print(dic)
if __name__ == '__main__':
    mlmet = Mlmet()
    mlmet.print_info()
