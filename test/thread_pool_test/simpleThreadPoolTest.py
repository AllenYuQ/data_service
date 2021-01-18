from concurrent.futures import ThreadPoolExecutor
import time

def get_html(times):
    time.sleep(times)
    print("get page1 {}s finished".format(times))
    return times
def get_html2(times):
    time.sleep(times)
    print("get page2 {}s finished".format(times))
    return times
if __name__ == '__main__':
    executor = ThreadPoolExecutor(max_workers=2)
    task1 = executor.submit(get_html, (1))
    task2 = executor.submit(get_html2, (4))
    time.sleep(5)
    print(task1.result())
    print(task2.result())