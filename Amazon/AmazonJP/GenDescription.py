#!/usr/bin/env python
# -*- coding: utf-8 -*-


# 1 ----------------导入模块
import sys
sys.path.append('..')
from Utils import *


# 2 ----------------节点与始末图片声明
image_begin = 'static_images/image_start.jpg'
image_end = 'static_images/image_end.jpg'
div_begin = '<div class="a-section a-spacing-medium a-spacing-top-small">'
div_end = '</div>'
img_rep = 'image_link'
img = '<img src="image_link">'
ul_begin = '<ul class="a-vertical a-spacing-none">'
ul_end = '</ul>'
li_begin = '<li><span class="a-list-item">'
li_end = '</span></li>'
br = '<br/>'


# 3 ----------------添加换行符
def addEnter(text):
    return text + '\n'


# 4 ----------------添加换行符
def genDescription(feature_list, image_list, product_feature_div_description_list,
                                 aplus_feature_div_description_list, comment_image_text_list):
    img = '<img src="image_link">'

    description = addEnter(div_begin)

    # 商家开始图片
    description += addEnter(img.replace(img_rep, image_begin))

    # 商品特点
    if feature_list and len(feature_list) > 0:
        description += addEnter(br)
        description += addEnter(br)
        description += addEnter(br)
        description += addEnter('商品特点：')
        description += addEnter(ul_begin)
        for feature in feature_list:
            description += li_begin
            description += feature
            description += addEnter(li_end)
        description += addEnter(ul_end)

    # 商品图片
    if image_list and len(image_list) > 0:
        description += addEnter(br)
        description += addEnter('商品图片：')
        for image in image_list:
            description += addEnter(br)
            description += addEnter(img.replace(img_rep, image))

    # 商品图片描述1
    if product_feature_div_description_list and len(product_feature_div_description_list) > 0:
        description += addEnter(br)
        description += addEnter('商家图片1：')
        for image in product_feature_div_description_list:
            if 'http' in image:
                description += addEnter(br)
                description += addEnter(img.replace(img_rep, image))

    # 商品图片描述2
    if aplus_feature_div_description_list and len(aplus_feature_div_description_list) > 0:
        description += addEnter(br)
        description += addEnter('商家图片2：')
        for image in aplus_feature_div_description_list:
            if 'http' in image:
                description += addEnter(br)
                description += addEnter(img.replace(img_rep, image))

    # 评论
    if comment_image_text_list and len(comment_image_text_list) > 0:
        description += addEnter(br)
        description += addEnter('评论图片：')
        for image in comment_image_text_list:
            description += addEnter(br)
            description += addEnter(img.replace(img_rep, image))

    # 商家末尾图片
    description += addEnter(br)
    description += addEnter(img.replace(img_rep, image_end))

    description += addEnter(div_end)
    #description = u''
    println(description)

    return description

# 4.1 方法测试
# genDescription(None, None, None, None)