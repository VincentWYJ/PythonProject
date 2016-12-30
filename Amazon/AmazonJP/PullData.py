# -*- coding: utf-8 -*-


# 1 ----------------模块导入
import re
import datetime
from bs4 import BeautifulSoup
import sys
sys.path.append('..')
from Utils import *


# 2 ----------------常量定义
# 汇率(API)
exchange_rate = 15
# 利润率(可调)
profit_rate = 0.3
# 包装重量(克)
packet_weight = 150
# 产地后缀
title_append = u'日本制造'
# 描述头
description_start = 'xxx'
# 描述尾
description_end = 'yyy'


# 3 ----------------数据获取
def pullData(html_url):
    println(u'\n\n打印获取数据------------------------------------------------')

    # 商品总信息列表
    product_info_list = []

    # 商品总信息字典
    product_info_dict = {}

    # 提取网页内容
    html_url = 'Htmls/' + html_url
    html_file = open(html_url, encoding='UTF-8')
    bs_obj = BeautifulSoup(html_file.read(), 'html.parser')

    # 排除script脚本
    for script in bs_obj(['script', 'style']):
        script.extract()

    # 3.1 宝贝名称
    print(u'title--宝贝名称: ')
    title = ''
    title_node = bs_obj.find('', {'id': 'productTitle'})
    if title_node and len(title_node) > 0:
        title = translate(title_node.get_text().strip().replace('\'', ''))
    title = title_append + title
    product_info_dict['title'] = title
    product_info_list.append(title)
    println(u'宝贝名称: %s' % title)

    # 3.2 宝贝类目
    cid = 50018961
    product_info_dict['cid'] = cid
    product_info_list.append(cid)
    println(u'宝贝类目: %d' % cid)

    # 3.3 店铺类目
    seller_cids = 50018961
    product_info_dict['seller_cids'] = seller_cids
    product_info_list.append(seller_cids)
    println(u'店铺类目: %d' % seller_cids)

    # 3.4 淘宝新旧程度
    stuff_status = 1
    product_info_dict['stuff_status'] = stuff_status
    product_info_list.append(stuff_status)
    println(u'新旧程度: %d' % stuff_status)

    # 3.5 省
    location_state = u'海外'
    product_info_dict['location_state'] = location_state
    product_info_list.append(location_state)
    println(u'省: %s' % location_state)

    # 3.6 城市
    location_city = u'日本'
    product_info_dict['location_city'] = location_city
    product_info_list.append(location_city)
    println(u'城市: %s' % location_city)

    # 3.7 出售方式
    item_type = 1
    product_info_dict['item_type'] = item_type
    product_info_list.append(item_type)
    println(u'出售方式: %d' % item_type)

    # 3.8 宝贝价格
    # 3.8.1 原价
    print(u'src_price--原价: ')
    src_price = 0
    src_price_node = bs_obj.find('', {'id': 'priceblock_ourprice'})
    if src_price_node and len(src_price_node) > 0:
        src_price = int(src_price_node.get_text().replace('￥', '').replace(',', '').strip())
    println(src_price)

    # 3.8.2 配送费
    print(u'ship_price--配送费: ')
    ship_price = 500
    ship_price_node = bs_obj.find('', {'id': 'price-shipping-message'})
    if ship_price_node and len(ship_price_node) > 0:
        ship_price_text = ship_price_node.get_text().replace('\n', '').strip()
        if u'配送無料' in ship_price_text:
            if '¥' not in ship_price_text:
                ship_price = 0
    println(ship_price)

    # 3.8.3 产品详细
    print(u'detail_dict--商品详细: ')
    detail_label_list = []
    detail_value_list = []
    detail_node = bs_obj.find('', {'id': 'prodDetails'})
    if detail_node and len(detail_node) > 0:
        for label_text in detail_node.find_all('td', {'class': 'label'}):
            if label_text != '\n':
                label = translate(label_text.get_text().strip().replace('\n', ''))
                detail_label_list.append(label)
        for value_text in detail_node.find_all('td', {'class': 'value'}):
            if value_text != '\n':
                value = translate(value_text.get_text().strip().replace('\n', ''))
                detail_value_list.append(value)
        if len(detail_label_list) > 0 and len(detail_value_list) > 0:
            for index in range(len(detail_label_list)):
                println('%s: %s' % (detail_label_list[index], detail_value_list[index]))
    if len(detail_label_list) == 0 or len(detail_value_list) == 0:
        println('无')

    # 3.8.4 价格计算
    weight = detail_value_list[detail_label_list.index(u'重量')]
    weight = int(weight.replace(u'克', '').strip())
    if (weight + packet_weight) < 500:
        ems = 100
    else:
        ems = 100 + ((weight + packet_weight - 500) / 100) * 10
    price = round(((src_price + ship_price) / exchange_rate + (ems)) * (1 + profit_rate))
    product_info_dict['price'] = price
    product_info_list.append(price)
    println(u'宝贝价格: %d' % price)

    # 3.9 加价幅度
    auction_increment = 0
    product_info_dict['auction_increment'] = auction_increment
    product_info_list.append(auction_increment)
    println(u'加价幅度: %d' % auction_increment)

    # 3.10 宝贝数量
    num = 0
    num_node = bs_obj.find('', {'id': 'availability'})
    if num_node and len(num_node) > 0:
        num_text = num_node.get_text().replace('\n', '').strip()
        if u'在庫あり' in num_text:
            num = 50
        elif u'残り' in num_text:
            num = 5
        elif u'月以内' in num_text:
            num = 0
        elif u'日以内' in num_text:
            num = 1
    product_info_dict['num'] = num
    product_info_list.append(num)
    println(u'宝贝数量: %d' % num)

    # 3.11 有效期
    now = datetime.datetime.today() + datetime.timedelta(days=6)
    valid_thru = now.strftime('%Y/%m/%d %H:%M')
    product_info_dict['valid_thru'] = valid_thru
    product_info_list.append(valid_thru)
    println(u'有效期: %s' % valid_thru)

    # 3.12 运费承担
    freight_payer = 2
    product_info_dict['freight_payer'] = freight_payer
    product_info_list.append(freight_payer)
    println(u'运费承担: %d' % freight_payer)

    # 3.13 平邮
    post_fee = 0
    product_info_dict['post_fee'] = post_fee
    product_info_list.append(post_fee)
    println(u'平邮: %d' % post_fee)

    # 3.14 EMS
    ems_fee = 2
    product_info_dict['ems_fee'] = ems_fee
    product_info_list.append(ems_fee)
    println(u'EMS: %d' % ems_fee)

    # 3.15 快递
    express_fee = 0
    product_info_dict['express_fee'] = express_fee
    product_info_list.append(express_fee)
    println(u'快递: %d' % express_fee)

    # 3.16 发票
    has_invoice = 1
    product_info_dict['has_invoice'] = has_invoice
    product_info_list.append(has_invoice)
    println(u'发票: %d' % has_invoice)

    # 3.17 保修
    has_warranty = 1
    product_info_dict['has_warranty'] = has_warranty
    product_info_list.append(has_warranty)
    println(u'保修: %d' % has_warranty)

    # 3.18 放入仓库
    approve_status = 1
    product_info_dict['approve_status'] = approve_status
    product_info_list.append(approve_status)
    println(u'放入仓库: %d' % approve_status)

    # 3.19 橱窗推荐
    has_showcase = 0
    product_info_dict['has_showcase'] = has_showcase
    product_info_list.append(has_showcase)
    println(u'橱窗推荐: %d' % has_showcase)

    # 品牌
    print(u'brand--品牌: ')
    brand = ''
    brand_node = bs_obj.find('', {'id': 'brand'})
    if brand_node and len(brand_node) > 0:
        brand = translate(brand_node.get_text().strip().replace('\'', ''))
    println(brand)

    # 产品特点
    print(u'feature_list--产品特点: ')
    feature_list = []
    feature_node = bs_obj.find('', {'id': 'feature-bullets'})
    if feature_node and len(feature_node) > 0:
        for feature_text in feature_node.find_all('span'):
            if feature_text != '\n':
                feature = translate(feature_text.get_text().replace('\n', '').replace('\'', '').strip())
                feature_list.append(feature)
                println(feature)
    if len(feature_list) == 0:
        println(u'无')

    # 图片地址
    print(u'image_list--图片地址: ')
    image_list = []
    image_node = bs_obj.find('', {'id': 'altImages'})
    if image_node and len(image_node) > 0:
        for image_text in image_node.find_all('img'):
            if image_text != '\n':
                image = image_text.get('src').replace('SS40', 'SL780')
                image_list.append(image)
                println(image)
    if len(image_list) == 0:
        println(u'无')

    # 商品图片描述
    print(u'description_list--商品图片描述: ')
    description_image_list = []
    description_node = bs_obj.find('', {'id': 'productDescription'})
    replace_reg = re.compile(r'_UX...')
    if description_node and len(description_node) > 0:
        for image_text in description_node.find_all('img'):
            if image_text != '\n':
                image = replace_reg.sub('_UX780', image_text.get('src'))
                description_image_list.append(image)
                println(image)
    if len(description_image_list) == 0:
        println(u'无')

    # 商品问答环节
    print(u'question_dict--商品问答环节: ')
    question_list = []
    answer_list = []
    question_node = bs_obj.find('', {'id': 'cf-ask-cel'})
    if question_node and len(question_node) > 0:
        for question in question_node.find_all('a', href=re.compile(r'.*asin.*')):
            if question != '\n':
                question_list.append(translate(question.get_text().strip()))
        for answer in question_node.find_all('span', href=re.compile(r'.*asin.*')):
            if answer != '\n':
                answer_list.append(translate(answer.get_text().strip()))
        if len(question_list) > 0 and len(answer_list) > 0:
            for index in range(len(question_list)):
                println('%s: %s' % (question_list[index], answer_list[index]))
    if len(question_list) == 0 or len(answer_list) == 0:
        println(u'无')

    # 客户图片评论
    print(u'comment_image_list--客户图片评论: ')
    comment_image_list = []
    comment_node = bs_obj.find('', {'id': 'revMH'})
    replace_reg = re.compile(r'_SL...')
    if comment_node and len(comment_node) > 0:
        for image_text in comment_node.find_all('img'):
            if image_text != '\n':
                image = replace_reg.sub('_SL780', image_text.get('src'))
                comment_image_list.append(image)
                println(image)
    if len(comment_image_list) == 0:
        println(u'无')

    # 客户文字评论
    print(u'comment_text_list--客户文字评论: ')
    comment_text_list = []
    comment_node = bs_obj.find('',{'id':'revMH'})
    for aa in bs_obj(['a']):
        aa.extract()
    if comment_node and len(comment_node) > 0:
        for comment_text in comment_node.find_all('div',{'class':'a-section celwidget'}):
            if comment_text != '\n':
                comment = comment_text.get_text().replace('\n', '').strip()
                comment_text_list.append(comment)
                println(comment)
    if len(comment_text_list) == 0:
        println('无')

    print(u'商品信息字典形式: ')
    println(product_info_dict)
    print(u'商品信息列表形式: ')
    println(product_info_list)

    return product_info_list





