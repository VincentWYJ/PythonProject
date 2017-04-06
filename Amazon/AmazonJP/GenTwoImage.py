#!/usr/bin/env python
# -*- coding: utf-8 -*-


# 1 ----------------模块导入
import urllib.request


image_list = ['https://img.alicdn.com/imgextra/i1/32546558/TB25W7YbX5N.eBjSZFmXXboSXXa_!!32546558.jpg',\
              'https://img.alicdn.com/imgextra/i3/32546558/TB26DH4aW9I.eBjy0FeXXXqwFXa_!!32546558.jpg']
name = ['image_start.jpg', 'image_end.jpg']


# 2 ----------------生成tbi格式图片
def genImage():
    for i in list(range(len(image_list))):
        urllib.request.urlretrieve(image_list[i], name[i])


# 3 ----------------方法测试
genImage()