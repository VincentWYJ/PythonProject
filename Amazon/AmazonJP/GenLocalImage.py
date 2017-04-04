#!/usr/bin/env python
# -*- coding: utf-8 -*-


# 1 ----------------模块导入
import os
import sys
import shutil
import re
from PIL import Image
import urllib.request
from ImageReSize import *

sys_path = sys.path[0]
dir_temp_path = sys.path[0] + '/temp/'
dir_path = sys.path[0] + '/Items/'
#start_name = dir_path+'/805567564a7xxxx'
#format = '.tbi'
image_format_left = u'_SL'
image_format_right= u'_'
change_imagesize_reg = re.compile("_.*_")

# 2 ----------------生成tbi格式图片
def GenLocalImage(imageLink, image_format): # image format 600 or 900
    return_name_temp = dir_temp_path + imageLink.replace('https://','').replace('/','_')
    return_name = dir_path + imageLink.replace('https://', '').replace('/', '_')
    formated_image_format = image_format_left + str(image_format) + image_format_right
    formated_imageLink = change_imagesize_reg.sub(formated_image_format, imageLink)
    try:
        urllib.request.urlretrieve(formated_imageLink, return_name_temp) #获取规定格式的图片
    except: # 应该加异常保护.....后面再完善
        urllib.request.urlretrieve(imageLink, return_name_temp) # 获取原始图片

    im = Image.open(return_name_temp)
    (x, y) = im.size
    x_s = x
    y_s = x / 600
    out = im.resize((x_s, y_s), Image.ANTIALIAS)
    out.save(return_name)

    return return_name
    # 3 ----------------方法测试
    # genImage(None)