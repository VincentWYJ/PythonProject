# -*- coding: utf-8 -*-


# 1 ----------------模块导入
import re
import datetime
from bs4 import BeautifulSoup
import sys
sys.path.append("..")
from Utils import *


# 2 ----------------常量定义
# 汇率(API)
exchange_rate = 15
# 利润率(可调)
profit_rate = 0.3
# 包装重量(克)
packet_weight = 150
# 产地后缀
title_append = '日本制造'
# 描述头
description_start = 'xxx'
# 描述尾
description_end = 'yyy'


# 3 ----------------数据获取
html_url = r'Html\2.htm'
html_file = open(html_url, encoding='UTF-8')
bs_obj = BeautifulSoup(html_file.read(), 'html.parser')

println('打印获取数据结果------------------------------------------------')

# 3.1
print('title--宝贝名称: ')
title_node = bs_obj.find('', {'id': 'productTitle'})
if title_node:
    title = translate(title_node.get_text().strip().replace('\'', ''))
else:
    title = ''
println(title)

# 3.2
print('brand--品牌: ')
brand_node = bs_obj.find('', {'id': 'brand'})
if brand_node:
    brand = translate(brand_node.get_text().strip().replace('\'', ''))
else:
    brand = ''
println(brand)

# 3.3
print('src_price--原价: ')
src_price_node = bs_obj.find('', {'id': 'priceblock_ourprice'})
if src_price_node:
    src_price = int(src_price_node.get_text().replace('￥', '').replace(',', '').strip())
else:
    src_price = 0
println(src_price)

# 3.4
print('ship_price--配送费: ')
ship_price_node = bs_obj.find('', {'id': 'price-shipping-message'})
if ship_price_node:
    ship_price = ship_price_node.get_text().replace('\n', '').strip()
    if '配送無料' in ship_price:
        if '¥' in ship_price:
            ship_price = 500
        else:
            ship_price = 0
    else:
        ship_price = 500
println(ship_price)

# 3.5
print('num--库存计数: ')
num_node = bs_obj.find('', {'id': 'availability'})
if num_node:
    num = num_node.get_text().replace('\n', '').strip()
else:
    num = ''
if '在庫あり' in num:
    num = 50
elif '残り' in  num:
    num = 5
elif '月以内' in num:
    num = 0
elif '日以内' in num:
    num = 1
else:
    num = 0
println(num)

# 3.6
print('feature_list--产品特点: ')
feature_list = []
feature_node = bs_obj.find('', {'id': 'feature-bullets'})
if feature_node:
    for feature in feature_node.find_all('span'):
        if feature != '\n':
            feature_list.append(translate(feature.get_text().replace('\n', '').replace('\'', '').strip()))
for feature in feature_list:
    println(feature)

# 3.7
print('image_list--图片地址: ')
image_list = []
image_node = bs_obj.find('', {'id': 'altImages'})
if len(image_node) > 0:
    for image in image_node.find_all('img'):
        if image != '\n':
            image_list.append(image.get('src').replace('SS40', 'SL780'))
for image in image_list:
    println(image)

# 3.8
print('detail_dict--商品详细: ')
detail_label_list = []
detail_value_list = []
detail_node = bs_obj.find('', {'id': 'prodDetails'})
if len(detail_node) > 0:
    for label in detail_node.find_all('td', {'class': 'label'}):
        if label != '\n':
            detail_label_list.append(translate(label.get_text().strip().replace('\n', '')))
    for value in detail_node.find_all('td', {'class': 'value'}):
        if value != '\n':
            detail_value_list.append(translate(value.get_text().strip().replace('\n', '')))
if len(detail_label_list) > 0 and len(detail_value_list) > 0:
    for index in range(len(detail_label_list)):
        println('%s: %s' %(detail_label_list[index], detail_value_list[index]))

# 3.9
print('description_list--商品图片描述: ')
description_image_list = []
description_node = bs_obj.find('', {'id': 'productDescription'})
replace_reg = re.compile(r'_UX...')
if len(description_node) > 0:
    for img in description_node.find_all('img'):
        if img != '\n':
            img = replace_reg.sub('_UX780', img.get('src'))
            description_image_list.append(img)
for image in description_image_list:
    println(image)

# 3.10
print('question_dict--商品问答环节: ')
question_list = []
answer_list = []
question_node = bs_obj.find('', {'id': 'cf-ask-cel'})
if len(question_node) > 0:
    for question in question_node.find_all('a', href=re.compile(r'.*asin.*')):
        if question != '\n':
            question_list.append(translate(question.get_text().strip()))
    for answer in question_node.find_all('span', href=re.compile(r'.*asin.*')):
        if answer != '\n':
            answer_list.append(translate(answer.get_text().strip()))
if len(question_list) > 0 and len(answer_list) > 0:
    for index in range(len(question_list)):
        println('%s: %s' % (question_list[index], answer_list[index]))

# 3.11
print('comment_image_list--客户图片评论: ')
comment_image_list = []
comments_node = bs_obj.find('', {'id': 'revMH'})
replace_reg = re.compile(r'_SL...')
if len(comments_node) > 0:
    for image in comments_node.find_all('img'):
        if image != '\n':
            image = replace_reg.sub('_SL780', image.get('src'))
            comment_image_list.append(image)
for image in comment_image_list:
    println(image)

# 3.12
print('comment_text_list--客户文字评论: ')
comment_text_list = []
comment_position = bs_obj.find('',{'id':'revMH'})
for aa in bs_obj(['a']):
    aa.extract()
for comment in comment_position.find_all('div',{'class':'a-section celwidget'}):
    if comment != '\n':
        comment_text_list.append(comment.get_text().replace('\n', '').strip())
for text in comment_text_list:
    println(text)


# 4 填充淘宝表格

println('打印写入数据结果------------------------------------------------')

# 商品总信息, 格式为dict--字典, 访问格式p[key] = value
product_info = {}

# 4.1 宝贝名称
title = title_append + title
product_info['title'] = title
println('宝贝名称: %s' %product_info['title'])

# 4.2 宝贝类目
cid = 50018961
product_info['cid'] = cid
println('宝贝类目: %d' %product_info['cid'])

# 4.3 店铺类目
seller_cids = 50018961
product_info['seller_cids'] = seller_cids
println('店铺类目: %d' %seller_cids)

# 4.4 淘宝新旧程度
stuff_status = 1
product_info['stuff_status'] = stuff_status
println('新旧程度: %d' %product_info['stuff_status'])

# 4.5 省
location_state = '海外'
product_info['location_state'] = location_state
println('省: %s' %product_info['location_state'])

# 4.6 城市
location_city = '日本'
product_info['location_city'] = location_city
println('城市: %s' %product_info['location_city'])

# 4.7 出售方式
item_type = 1
product_info['item_type'] = item_type
println('出售方式: %d' %product_info['item_type'])

# 4.8 宝贝价格
weight = detail_value_list[detail_label_list.index('重量')]
weight = int(weight.replace('克', '').strip())
if (weight + packet_weight) < 500:
    ems = 100
else:
    ems = 100 + ((weight + packet_weight -500) / 100)*10
price = round(((src_price + ship_price) / exchange_rate + (ems)) * (1 + profit_rate))
product_info['price'] = price
println('宝贝价格: %d' %product_info['price'])

# 4.9 加价幅度
auction_increment = 0
product_info['auction_increment'] = auction_increment
println('加价幅度: %d' %product_info['auction_increment'])

# 4.10 宝贝数量
num = num
product_info['num'] = num
println('宝贝数量: %d' %product_info['num'])

# 4.11 有效期
now = datetime.datetime.today() + datetime.timedelta(days = 6)
valid_thru = now.strftime('%Y/%m/%d %H:%M')
product_info['valid_thru'] = valid_thru
println('有效期: %s' %product_info['valid_thru'])

# 4.12 运费承担
freight_payer = 2
product_info['freight_payer'] = freight_payer
println('运费承担: %d' %product_info['freight_payer'])

# 4.13 平邮
post_fee = 0
product_info['post_fee'] = post_fee
println('平邮: %d' %product_info['post_fee'])

# 4.14 EMS
ems_fee = 2
product_info['ems_fee'] = ems_fee
println('EMS: %d' %product_info['ems_fee'])

# 4.15 快递
express_fee = 0
product_info['express_fee'] = express_fee
println('快递: %d' %product_info['express_fee'])

# 4.16 发票
has_invoice = 1
product_info['has_invoice'] = has_invoice
println('发票: %d'%product_info['has_invoice'])

# 4.17 保修
has_warranty = 1
product_info['has_warranty'] = has_warranty
println('保修: %d' %product_info['has_warranty'])

# 4.18 放入仓库
approve_status = 1
product_info['approve_status'] = approve_status
println('放入仓库: %d' %product_info['approve_status'])

# 4.19 橱窗推荐
has_showcase = 0
product_info['has_showcase'] = has_showcase
println('橱窗推荐: %d' %product_info['has_showcase'])
