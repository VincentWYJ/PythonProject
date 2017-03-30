#!/usr/bin/env python
# -*- coding: utf-8 -*-


# 1 ----------------模块导入
import os
import shutil
import urllib.request


dir_path = 'Items'
start_name = dir_path+'/805567564a7cbdc'
format = '.tbi'


# 2 ----------------生成tbi格式图片
def genImage(imageLink_list, asin_number):
    # 下载图片
    i = 0
    for link in imageLink_list:
        if i < 10:
            name = start_name + asin_number + '0' + str(i) + format
        else:
            name = start_name + asin_number + str(i) + format
        urllib.request.urlretrieve(link, name)
        i += 1

# 3 ----------------方法测试
# genImage(None)