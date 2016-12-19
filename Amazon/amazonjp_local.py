# -*- coding: utf-8 -*-

import os
import http.cookiejar
from lxml import etree
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request, urllib.parse, urllib.error
import re
import datetime
from Translation import translate
#-----------------------------------------------------
#contantance setting
exchange_rate = int(15) # 汇率
profit_margin = 0.3 # 利润率
packet_weight = int(150) # 包装重量
title_append = "日本制造"
description_start = "xxx"
description_end = "yyy"
# 1、网站登录操作
# login_url = 'https://www.amazon.co.jp/ap/signin?_encoding=UTF8&openid.assoc_handle=jpflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.co.jp%2F%3Fref_%3Dnav_ya_signin'
# values = {'email': '44059346@qq.com', 'password': '1qaz2wsx@19', 'submit': 'Login'}
# postdata = urllib.parse.urlencode(values).encode()
# user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
# headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}

# cookie_filename = 'cookie.txt'
# cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
# request = urllib.request.Request(login_url, postdata, headers)

# try:
    # response = opener.open(request)
    # page = response.read().decode()
# except urllib.error.URLError as e:
    # print(e.code, ':', e.reason)
    
# cookie.save(ignore_discard = True, ignore_expires = True)

# print("Cookie info: ")
# for item in cookie:
    # print('Name = ' + item.name)
    # print('Value = ' + item.value)


# 2、数据获取操作
url = r'D:\projects\amazon\2.htm'

htmlfile = open(url, 'r',encoding='UTF-8')

bsobj = BeautifulSoup(htmlfile.read(), "html.parser")

# kill all script and style elements
for script in bsobj(["script", "style"]):
    script.extract()    # rip it out

# ------------------------------------------------------

print("\nproduct title 标题: ")
title_node = bsobj.find_all("", {"id": "productTitle"})
# node is not exist mark it empty
if (title_node):
    title_am = title_node[0].get_text()
# node is exist and more than one mark it error
else:
    title_am = "error"
title_cn = translate(title_am).replace("'","")
print(title_cn)
# ------------------------------------------------------

print("\nproduct brand 品牌: ")
brand_node = bsobj.find_all("", {"id": "brand"})
# node is not exist mark it empty
if (brand_node):
    brand = brand_node[0].get_text().strip()
# node is exist and more than one mark it error
else:
    brand = "error"
brand_cn = translate(brand).replace("'","")
print(brand_cn)

# ------------------------------------------------------

print("\nproduct price normal 正常价格: ")
price_am_node = bsobj.find_all("", {"id": "priceblock_ourprice"})
# node is not exist mark it empty
if (price_am_node):
    price_am = int(price_am_node[0].get_text().replace("￥","").replace(",","").strip())
# node is exist and more than one mark it error
else:
    price_am = "error"


# ------------------------------------------------------
# ------------------------------------------------------

print("\nproduct shipping price 配送费: ")
shipping_price_node = bsobj.find_all("", {"id": "price-shipping-message"})
# node is not exist mark it empty
# node is exist and only one get it
shipping_am = int(500)
if (shipping_price_node):
    shipping_price = shipping_price_node[0].get_text().replace("\n","").strip()
    if "配送無料" in shipping_price :
        if "￥" in shipping_price :
            shipping_am = int(500)
        else:
            shipping_am = int(0)
    else:
        shipping_am = int(500)

# ------------------------------------------------------

print("\nproduct availability 库存情况: ")
availability_node = bsobj.find_all("", {"id": "availability"})
if (availability_node):
    availability = availability_node[0].get_text().replace("\n","").strip()
# node is exist and more than one mark it error
else:
    availability = "error"
if "在庫あり" in availability:
    num_am = int(50)
elif "残り" in  availability:
    num_am = int(5)
elif "月以内" in availability:
    num_am = int(0)
elif "日以内" in availability:
    num_am = int(1)
print(availability)

# ------------------------------------------------------

# ------------------------------------------------------

# print("\nproduct speical price 特色价格: ")
# price_special_node = bsobj.find_all("", {"id": "priceblock_saleprice"})
# # node is not exist mark it empty
# if (len(price_special_node) == 0):
#     price_special = "empty"
# # node is exist and only one get it
# elif (len(price_special_node) == 1):
#     price_special = price_special_node[0].get_text().strip()
# # node is exist and more than one mark it error
# else:
#     price_special = "error"
# print(price_special)

# ------------------------------------------------------
# print("\nproduct third part information ")
# third_part_list = []
# third_part_node = bsobj.find("", {"id": "soldByThirdParty"})
# if (third_part_node):
#     for third_part in third_part_node.find_all("span"):
#         if third_part != "\n":
#             third_part_list.append(third_part.get_text().strip().replace("\n",""))

# ------------------------------------------------------

# print("\nproduct ddm Delivery Message  是否直邮: ")
# ddm_delivery_node = bsobj.find_all("", {"id": "ddmDeliveryMessage"})
# # node is not exist mark it empty
# if (len(ddm_delivery_node) == 0):
#     ddm_delivery = "empty"
# # node is exist and only one get it
# elif (len(ddm_delivery_node) == 1):
#     ddm_delivery = ddm_delivery_node[0].get_text().replace("\n","").strip()
# # node is exist and more than one mark it error
# else:
#     ddm_delivery = "error"
# print(ddm_delivery)

# ------------------------------------------------------

# ------------------------------------------------------



# ------------------------------------------------------

# print("\nproduct availability 快递单位: ")
# merchant_node = bsobj.find_all("", {"id": "merchant-info"})
# # node is not exist mark it empty
# if (len(merchant_node) == 0):
#     merchant = "empty"
# # node is exist and only one get it
# elif (len(merchant_node) == 1):
#     merchant = merchant_node[0].get_text().replace("\n","").strip()
# # node is exist and more than one mark it error
# else:
#     merchant = "error"
# print(merchant)

# ------------------------------------------------------

# ------------------------------------------------------
print("\nproduct feature 产品特点: ")
feature_list = []
feature_list_cn = []
feature_node = bsobj.find("", {"id": "feature-bullets"})
if (feature_node):
    for features in feature_node.find_all("span"):
        if (features != "\n"):
            feature_list.append(features.get_text().replace("\n","").strip())

for info in feature_list:
    info_cn = translate(info).replace("'","").strip()
    feature_list_cn.append(info_cn)
    print(info_cn)
# ------------------------------------------------------

# ------------------------------------------------------
print("\nproduct image 图片地址: ")
image_list = []
images_node = bsobj.find("", {"id": "altImages"})
if (len(images_node) != 0):
    for images in images_node.find_all("img"):
        if images != "\n":
            image_list.append(images.get('src').replace("SS40","SL780"))  # get the attrs

for info in image_list:
    print(info)
# ------------------------------------------------------

# ------------------------------------------------------
print("\nproduct prodDetails 信息: ")
details_label_list = []
details_label_list_cn = []
details_value_list = []
details_value_list_cn = []
details_node = bsobj.find("", {"id": "prodDetails"})
if (len(details_node) != 0):
    for details_label in details_node.find_all("td", {"class": "label"}):
        if details_label != "\n":
            details_label_list.append(details_label.get_text().strip().replace("\n",""))
    for details_value in details_node.find_all("td", {"class": "value"}):
        if details_value != "\n":
            details_value_list.append(details_value.get_text().strip().replace("\n",""))

# -----------------------------------------------------
# 获取基本属性
ASIN = details_value_list[details_label_list.index("ASIN")]
Weight = details_value_list[details_label_list.index("発送重量")]
weight_am = int(Weight.replace("g","").strip())
Favorite_degree = details_value_list[details_label_list.index("おすすめ度")]
degree_reg = re.compile(r'5つ星のうち.....')
Favorite_degree_am = (degree_reg.search(Favorite_degree).group()).replace("5つ星のうち","").strip()
Category = details_value_list[details_label_list.index("Amazon 売れ筋ランキング")]
start_date = details_value_list[details_label_list.index("Amazon.co.jp での取り扱い開始日")]
print(ASIN)
print(weight_am)
print(Favorite_degree_am)
print(Category)
print(start_date)
# 删除基本属性
details_label_list.remove("ASIN")
details_value_list.remove(ASIN)
details_label_list.remove("発送重量")
details_value_list.remove(Weight)
details_label_list.remove("おすすめ度")
details_value_list.remove(Favorite_degree)
details_label_list.remove("Amazon 売れ筋ランキング")
details_value_list.remove(Category)
details_label_list.remove("Amazon.co.jp での取り扱い開始日")
details_value_list.remove(start_date)
#打印普通属性
for info in details_label_list:
    info_cn = translate(info)
    details_label_list_cn.append(info_cn)
    print(info_cn)
for info in details_value_list:
    info_cn = translate(info)
    details_value_list_cn.append(info_cn)
    print(info_cn)

# ------------------------------------------------------
print("\nproduct productDescription 商家详细信息: ")  # 文字需要和图像匹配，各种表格格式表达复杂，难以通用提取，故不提取文字。
pd_image_list = []
pd_node = bsobj.find("", {"id": "productDescription"})
replace_reg = re.compile(r'_UX...')
if (len(pd_node) != 0):
    for pd_image in pd_node.find_all("img"):
        if pd_image != "\n":
            pd_image_get= replace_reg.sub('_UX780', pd_image.get('src'))
            pd_image_list.append(pd_image_get)
for info in pd_image_list:
    print(info)
# -----------------------------------------------------



# ------------------------------------------------------
print("\nproduct Q&A 商品问答环节: ")

pd_question_list = []
pd_answer_list = []
qanda_node = bsobj.find("", {"id": "cf-ask-cel"})  # 用户经常问到的
if (len(qanda_node) != 0):
    for pd_question in qanda_node.find_all("a", href=re.compile(r".*asin.*")):
        if pd_question != "\n":
            pd_question_list.append(pd_question.get_text().strip())
    for pd_answer in qanda_node.find_all("span", href=re.compile(r".*asin.*")):
        if pd_answer != "\n":
            pd_answer_list.append(pd_answer.get_text().strip())

for info in pd_question_list:
    print(info)
for info in pd_answer_list:
    print(info)
# -----------------------------------------------------

print("\nproduct comments 客户评论图片: ")
comments_picture_list = []
comments_picture_node = bsobj.find("", {"id": "revMH"})
replace_reg = re.compile(r'_SL...')
if (len(comments_picture_node) != 0):
    for comments_picture in comments_picture_node.find_all("img"):
        if comments_picture != "\n":
            comments_picture_get = replace_reg.sub('_SL780', comments_picture.get('src'))
            comments_picture_list.append(comments_picture_get)
for info in comments_picture_list:
    print(info)
# -----------------------------------------------------

print("\nproduct comments 客户评论: ")
comments_list = []
comments_position = bsobj.find("",{"id":"revMH"})
for aa in bsobj(["a"]):
    aa.extract()    # rip it out
for comments in comments_position.find_all("div",{"class":"a-section celwidget"}):
    if comments != "\n":
        comments_list.append(comments.get_text().replace("\n","").strip())
for info in comments_list:
        print(info)


#-----------------------------------------------------

# 填充淘宝表格

#-----------------------------------------------------
# 淘宝标题
#-----------------------------------------------------
title = title_append+title_cn
print("\n淘宝标题：%s"%title)
#-----------------------------------------------------
# 淘宝宝贝类目
#-----------------------------------------------------
cid = int(50018961)
print("\n淘宝宝贝类目: %d"%cid)
#-----------------------------------------------------
# 淘宝宝贝类目
#-----------------------------------------------------
seller_cids = int(50018961)
print("\n淘宝店铺类目: %d"%seller_cids)
#-----------------------------------------------------
# 淘宝新旧程度
#-----------------------------------------------------
stuff_status = int(1)
print("\n淘宝新旧程度: %d"%stuff_status)
#-----------------------------------------------------
# 淘宝物品所在省
#-----------------------------------------------------
location_state = "海外"
print("\n淘宝物品所在省: %s"%location_state)
#-----------------------------------------------------
# 淘宝物品所在省
#-----------------------------------------------------
location_city = "日本"
print("\n淘宝物品所在市: %s"%location_city)
#-----------------------------------------------------
# 淘宝物品出售方式
#-----------------------------------------------------
item_type = int(1)
print("\n淘宝物品出售方式: %d"%item_type)
#-----------------------------------------------------
# 淘宝宝贝价格
#-----------------------------------------------------
# 计算EMS邮费
if ((weight_am + packet_weight) < 500):
    Ems = 100
else:
    Ems = 100 + ((weight_am + packet_weight -500)/100)*10
# 计算售价
price = round(((price_am + shipping_am) / exchange_rate + (Ems)) * (1 + profit_margin))
print("\n预计淘宝售价是: %d"%price)
#-----------------------------------------------------
# 淘宝物品加价幅度
#-----------------------------------------------------
auction_increment = int(0)
print("\n淘宝物品加价幅度: %d"%auction_increment)
#-----------------------------------------------------
# 淘宝物品数量
#-----------------------------------------------------
num = num_am
print("\n淘宝宝贝数量: %d"%num)
#-----------------------------------------------------
# 淘宝有效期
#-----------------------------------------------------
#获得当前时间
now = datetime.datetime.today()+datetime.timedelta(days = 6) #->这是时间数组格式
#转换为指定的格式:
valid_thru = now.strftime("%Y/%m/%d %H:%M")
print("\n淘宝有效期: %s"%valid_thru)
#-----------------------------------------------------
# 淘宝运费承担
#-----------------------------------------------------
freight_payer = int(2)
print("\n淘宝承担邮费: %d"%freight_payer)
#-----------------------------------------------------
# 淘宝运费承担
#-----------------------------------------------------
post_fee = int(0)
print("\n淘宝平邮: %d"%post_fee)
#-----------------------------------------------------
# 淘宝EMS
#-----------------------------------------------------
ems_fee = int(2)
print("\n淘宝EMS: %d"%ems_fee)
#-----------------------------------------------------
# 淘宝快递
#-----------------------------------------------------
express_fee = int(0)
print("\n淘宝快递: %d"%express_fee)
#-----------------------------------------------------
# 淘宝发票
#-----------------------------------------------------
has_invoice = int(1)
print("\n淘宝发票: %d"%has_invoice)
#-----------------------------------------------------
# 淘宝保修
#-----------------------------------------------------
has_warranty = int(1)
print("\n淘宝保修: %d"%has_warranty)
#-----------------------------------------------------
# 淘宝放入仓库
#-----------------------------------------------------
approve_status = int(1)
print("\n淘宝放入仓库: %d"%approve_status)
#-----------------------------------------------------
# 淘宝橱窗推荐
#-----------------------------------------------------
has_showcase = int(0)
print("\n淘宝橱窗推荐: %d"%has_showcase)
#-----------------------------------------------------
# 淘宝运费承担
#-----------------------------------------------------
# list_time = int(2)
# print("\n开始时间: %d"%list_time)
#-----------------------------------------------------
# 淘宝详细描述
#-----------------------------------------------------
description = int(2)

if (feature_list_cn):
    for feature_list in feature_list_cn:
        description = description+ feature_list


print("\淘宝橱窗推荐: %d"%description)
