from concurrent.futures import ThreadPoolExecutor
import queue
import time
from utils.crawl_data.my_crawl_data import get_craw_data
if __name__ == '__main__':
    executor =ThreadPoolExecutor(max_workers=2)
    task1 = executor.submit(get_craw_data())
    print("done")

