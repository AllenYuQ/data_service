import sys
import os
dir=os.path.abspath('..')
sys.path.append(dir)
import requests
import yaml
from utils.logging.getLogger import GetLogger
logger = GetLogger(logs_dir='./logs').get_logger()
#初始化操作，下次应该单独写一个初始化的过程

def sendMsgToGo():
    logger.info("通知go server 生产消息")
    try:
        url = 'http://172.16.0.15:8098/go_python'
        #url = 'http://127.0.0.1:8088/go_python'
        d = {'hasDone': 'yes'}
        r = requests.post(url, data=d)
        result = r.text
        logger.info("go server" + result)
    except:
        result = ""
        logger.info("go server 通知失败!")
    return result

if __name__ == '__main__':
    sendMsgToGo()
