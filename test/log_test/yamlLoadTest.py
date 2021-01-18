import yaml
import os
import sys
dir=os.path.abspath('../..')
sys.path.append(dir)

if __name__ == '__main__':
   try:
       f = open("../../config/dbSetting")
       data = yaml.load(f, Loader=yaml.FullLoader)
       print(data)
       f.close()
   except Exception:
       print("未找到yaml文件")
