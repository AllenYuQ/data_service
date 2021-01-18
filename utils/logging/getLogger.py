from concurrent_log import ConcurrentTimedRotatingFileHandler
import logging
import os
import re

class GetLogger:
    """
    自定义logging，方便使用
    """

    def __init__(self, logs_dir=None, logs_level=logging.INFO):
        self.logs_dir = logs_dir  # 日志路径
        self.log_name = r'app.log'  # 日志名称
        self.logs_level = logs_level  # 日志级别
        # 日志的输出格式
        self.log_formatter = logging.Formatter(
            '%(asctime)s [%(filename)s] [%(funcName)s] [%(levelname)s] [%(lineno)d] %(message)s')

        if logs_dir is None:
            sep = os.sep  # 自动匹配win,mac,linux 下的路径分隔符
            self.logs_dir = os.path.abspath(
                os.path.join(__file__, f"..{sep}..{sep}logs{sep}"))  # 设置日志保存路径

        # 如果logs文件夹不存在，则创建
        if os.path.exists(self.logs_dir) is False:
            os.mkdir(self.logs_dir)

    def get_logger(self):
        """在logger中添加日志句柄并返回，如果logger已有句柄，则直接返回"""
        # 实例化root日志对象
        log_logger = logging.getLogger('root')

        # 设置日志的输出级别
        log_logger.setLevel(self.logs_level)
        if not log_logger.handlers:  # 避免重复日志
            # 创建一个handler，用于输出到cmd窗口控制台
            console_handler = logging.StreamHandler()

            console_handler.setLevel(logging.INFO)  # 设置日志级别
            console_handler.setFormatter(self.log_formatter)  # 设置日志格式
            log_logger.addHandler(console_handler)

            # 建立一个循环文件handler来把日志记录在文件里
            file_handler = ConcurrentTimedRotatingFileHandler(
                filename=self.logs_dir + os.sep + self.log_name,  # 定义日志的存储
                when="MIDNIGHT",  # 按照日期进行切分when = D： 表示按天进行切分,or self.when == 'MIDNIGHT'
                interval=1,  # interval = 1： 每天都切分。 比如interval = 2就表示两天切分一下。
                backupCount=30,  # 最多存放日志的数量
                encoding="UTF-8",  # 使用UTF - 8的编码来写日志
                delay=False,
                utc=False  # 使用UTC + 0的时间来记录 （一般docker镜像默认也是UTC + 0）
            )
            file_handler.suffix = "%Y-%m-%d.log"
            # need to change the extMatch variable to match the suffix for it
            file_handler.extMatch = re.compile(r"^\d{8}$")
            file_handler.setLevel(logging.DEBUG)  # 设置日志级别
            file_handler.setFormatter(self.log_formatter)  # 设置日志格式
            file_handler.doRollover()
            log_logger.addHandler(file_handler)

        return log_logger
