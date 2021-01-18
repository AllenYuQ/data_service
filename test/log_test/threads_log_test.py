import threading, time
from test.log_test.simple_log_test import GetLogger
class SubThread(threading.Thread):
    def run(self):
        while True:
            logger = GetLogger().get_logger()
            logger.info('INFO日志打印...')
            logger.error('ERROR日志打印...')
            time.sleep(1)
if __name__ == '__main__':
    logger = GetLogger().get_logger()
    t1 = SubThread()
    t2 = SubThread()
    t1.start()
    t2.start()

