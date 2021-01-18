from apscheduler.schedulers.background import BlockingScheduler
from utils.crawl_data.my_crawl_data import get_craw_data
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import threading
import time
from queue import Queue
myQueue = Queue()

def job1():
    myQueue.put(1)
    print('job1')


def job2(x, y):
    while myQueue.empty() == True:
        print("还没有")
        time.sleep(1)
    myQueue.get()
    print('job2', x, y)
    myQueue.task_done()
    #sum = 2 / 0

def job3():
    print('每隔1小时执行一次')

def my_listener(event):
    if event.exception:
        print("保存出错信息")
        # 如果出现失误，首先将出错的消息发给服务器
        # 日志记录下来
        #1.直接关闭任务调度器
        scheduler.resume()
        print("任务出错了!!!")
    else:
        print('任务照常进行...')
if __name__ == '__main__':

    scheduler = BlockingScheduler()

    scheduler.add_job(
        job2,
        trigger='cron',
        second='*/5',
        args=['hello', 'world']
    )

    scheduler.add_job(
        job1,
        trigger='cron',
        second='*/5'
    )
    #每天整点运行
    # scheduler.add_job(
    #     get_craw_data,
    #     trigger='cron',
    #     #hour='0-23',
    #     minute='0-59',
    # )
    scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.start()