#!/usr/bin/env python
# -*- coding: utf-8 -*-


# 1 ----------------模块导入
import os
import sys
import shutil
import re
from  PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import urllib.request

sys_path = sys.path[0]
dir_temp_path = sys.path[0] + '/temp/'
dir_path = sys.path[0] + '/Items/'
#start_name = dir_path+'/805567564a7xxxx'
#format = '.tbi'
image_format_left = u'._SL'
image_format_right= u'_'
change_imagesize_reg = re.compile("\._.*_")

# 2 ----------------生成tbi格式图片
def GenLocalImage(imageLink, image_format): # image format 600 or 900
    return_name_temp = dir_temp_path + imageLink.replace('https://','').replace('/','_')
    return_name = dir_path + imageLink.replace('https://', '').replace('/', '_')
    formated_image_format = image_format_left + str(image_format) + image_format_right
    formated_imageLink = change_imagesize_reg.sub(formated_image_format, imageLink)
    # 处理多个图片链接连在一起的情况
    if '"' in return_name_temp:
        print('########################################################')
        print(return_name_temp)
        return_name_temp = return_name_temp.replace('"', '')
        print(return_name_temp)
    if '"' in return_name:
        print('########################################################')
        print(return_name)
        return_name = return_name.replace('"', '')
        print(return_name)
    if '"' in formated_imageLink:
        print('########################################################')
        print(formated_imageLink)
        formated_imageLink = formated_imageLink[0, formated_imageLink.find('"')] + "'"
        print(formated_imageLink)
    try:
        urllib.request.urlretrieve(formated_imageLink, return_name_temp) #获取规定格式的图片
    except: # 应该加异常保护.....后面再完善
        urllib.request.urlretrieve(imageLink, return_name_temp) # 获取原始图片
    try:
        imageopened = Image.open(return_name_temp)
        x,y = imageopened.size
        x_s = image_format
        y_s = int((y / x) * image_format)
        imagesaved = imageopened.resize((x_s, y_s))
        imagesaved.save(return_name)
    except IOError:
        println(u'图片处理模块文件IO错误')
    return return_name
    # 3 ----------------方法测试
    # genImage(None)