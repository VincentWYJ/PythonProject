# -*- coding: utf-8 -*-


# 1 ----------------导入模块
import threading
import sys
sys.path.append('..')
from Utils import *
from PullHtml import pullHtml
from PullData import pullData
from PushData import pushData
import time
import os
import shutil


# 2 ----------------数据获取与写入
def pullAndPushData(html_url):
    product_info_list = pullData(html_url)
    pushData(product_info_list)


# 3 ----------------多线程处理
def startMutilThread():
    html_list = pullHtml()
    thread_list = []
    for html_url in html_list:
        thread_list.append(threading.Thread(target=pullAndPushData, args=(html_url,)))
    for thread in thread_list:
        thread.setDaemon(True)
        thread.start()
        time.sleep(20)
    thread.join()


# 4 ----------------初始化方法
if __name__ == '__main__':
    # 重置下载图片存在目录
    dir_path = 'Items'
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.mkdir(dir_path)

    # 开启多线程获取网页信息
    startMutilThread()