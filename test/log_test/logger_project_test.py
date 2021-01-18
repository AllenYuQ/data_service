import os
import sys
dir=os.path.abspath('..')
sys.path.append(dir)
import logging
from logging.handlers import TimedRotatingFileHandler
from concurrent_log import ConcurrentTimedRotatingFileHandler
from threading import Lock
import time, threading

class LoggerProject(object):
    def __init__(self, name):
        #self.mutex = Lock()
        self.formatter = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        self.name = name

    def _create_logger(self):
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(level=logging.INFO)
        #return self.logger

    def _file_logger(self):
        time_rotate_file = ConcurrentTimedRotatingFileHandler(filename='./time_rotate', when='S', interval=2, backupCount=5)
        time_rotate_file.setFormatter(logging.Formatter(self.formatter))
        time_rotate_file.setLevel(logging.INFO)
        return time_rotate_file

    def _console_logger(self):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level=logging.INFO)
        console_handler.setFormatter(logging.Formatter(self.formatter))
        return console_handler

    def pub_logger(self):
        self._create_logger()
        #self.mutex.acquire()
        self.logger.addHandler(self._file_logger())
        self.logger.addHandler(self._console_logger())
        #self.mutex.release()
        return self.logger

if __name__ == '__main__':
    log_pro1 = LoggerProject(name='allen')
    logger1 = log_pro1.pub_logger()
    log_pro2 = LoggerProject(name='jack')
    logger2 = log_pro2.pub_logger()
    #
    # logger1 = logging.getLogger("allen")
    # logger2 = logging.getLogger("jack")
    # logger1.setLevel(level=logging.INFO)
    # logger2.setLevel(level=logging.INFO)
    print(id(logger1))
    print(id(logger2))
    logger1.info("aaaa")
    logger2.info("bbbb")


