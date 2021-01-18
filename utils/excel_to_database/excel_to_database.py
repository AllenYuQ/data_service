import sys
import os
from dao.dbMlmet import DBMlmet
dir=os.path.abspath('..')
sys.path.append(dir)
import pandas as pd

if __name__ == '__main__':
    dbMlmet = DBMlmet()
    df = pd.read_excel("../../make_predicitions/wuxi_meteos.xlsx")
    for index, row in df.iterrows():
        dbMlmet.insert(row['time_point'], row['position_name'], row['precipitation'], row['temperature'], row['ws'],
                   row['wd'], row['humidity'], row['cloudrate'], row['skycon'], row['pressure'], row['visibility'],
                   row['dswrf'], row['aqi'], row['pm25'])
    dbMlmet.release_con()
