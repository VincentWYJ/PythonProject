# -*- coding: utf-8 -*-


# 1 ----------------导入模块
import sys
sys.path.append('..')
from Utils import *


# 2 ----------------节点与始末图片声明
image_begin = 'https://img.alicdn.com/imgextra/i1/32546558/TB25W7YbX5N.eBjSZFmXXboSXXa_!!32546558.jpg?t=1477750314000'
image_end = 'https://img.alicdn.com/imgextra/i3/32546558/TB26DH4aW9I.eBjy0FeXXXqwFXa_!!32546558.jpg?t=1477750314000'
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
def genWirelessDesc(title, feature_list, image_list, description_image_list, comment_image_list):

    description = addEnter(wap_begin)

    # 商品简述
    description += addEnter(short.replace(short_reg, title))

    # 商家开始图片
    description += addEnter(img.replace(img_reg, image_begin))

    # 商品特点
    if feature_list and len(feature_list) > 0:
        for feature in feature_list:
            description += addEnter(txt.replace(txt_reg, feature))

    # 商品图片
    if image_list and len(image_list) > 0:
        for image in image_list:
            description += addEnter(img.replace(img_reg, image))

    # 商家图片
    if description_image_list and len(description_image_list) > 0:
        for image in description_image_list:
            if 'http' in image:
                description += addEnter(img.replace(img_reg, image))
            elif u'了解更多' not in image:
                description += addEnter(txt.replace(txt_reg, image))

    # 评论图片
    if comment_image_list and len(comment_image_list) > 0:
        for image in comment_image_list:
            description += addEnter(img.replace(img_reg, image))

    # 商家末尾图片
    description += addEnter(img.replace(img_reg, image_end))

    description += addEnter(wap_end)

    println(description)

    return description

# 4.1 方法测试
# genWirelessDesc("", None, None, None, None)