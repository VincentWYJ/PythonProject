#!/usr/bin/env python
# -*- coding: utf-8 -*-


# 1 ----------------导入模块
import sys
import re
sys.path.append('..')
from Utils import *
from GenLocalImage import *


# 2 ----------------节点与始末图片声明
image_begin = 'static_images/image_start.jpg'
image_end = 'static_images/image_end.jpg'
wap_begin = '<wapDesc>'
wap_end = '</wapDesc>'
short = '<shortDesc>short_content</shortDesc>'
short_reg = 'short_content'
txt = '<txt>text_content</txt>'
txt_reg = 'text_content'
img = '<img>img_content</img>'
img_reg = 'img_content'


# 3 ----------------添加换行符
def addEnter(text):
    return text + '\n'


# 4 ----------------添加换行符
def genWirelessDesc(title, feature_list, image_list, product_feature_div_description_list,
                                 aplus_feature_div_description_list, comment_image_text_list):

    description = addEnter(wap_begin)

    # 商品简述
    description += addEnter(short.replace(short_reg, title))

    # 商家开始图片
    description += addEnter(img.replace(img_reg, image_begin))

    # 商品特点
    if feature_list and len(feature_list) > 0:
        for feature in feature_list:
            if u'请输入型号验证' not in feature:
                description += addEnter(txt.replace(txt_reg, feature))

    # 商品图片
    if image_list and len(image_list) > 0:
        for image in image_list:
            local_image = GenLocalImage(image, 600)
            description += addEnter(img.replace(img_reg, local_image))

    # 商品描述1
    if product_feature_div_description_list and len(product_feature_div_description_list) > 0:
        for content in product_feature_div_description_list:
            if re.search(r'.*http.*',content) != None:
                local_image = GenLocalImage(content, 600)
                description += addEnter(img.replace(img_reg, local_image))
            else:
                description += addEnter(txt.replace(txt_reg, str(content)))

    # 商品描述2
    if aplus_feature_div_description_list and len(aplus_feature_div_description_list) > 0:
        for content in aplus_feature_div_description_list:
            if 'http' in content:
                local_image = GenLocalImage(content, 600)
                description += addEnter(img.replace(img_reg, local_image))
            # elif u'了解更多' not in content:
            else:
                description += addEnter(txt.replace(txt_reg, content))

    # 评论
    if comment_image_text_list and len(comment_image_text_list) > 0:
        for content in comment_image_text_list:
            if 'http' in content:
                local_image = GenLocalImage(content, 600)
                description += addEnter(img.replace(img_reg, local_image))
            # elif u'了解更多' not in content:
            else:
                description += addEnter(txt.replace(txt_reg, content))

    # 商家末尾图片
    description += addEnter(img.replace(img_reg, image_end))

    description += addEnter(wap_end)

    #description = u''

    println(description)

    return description

# 4.1 方法测试
# genWirelessDesc("", None, None, None, None)