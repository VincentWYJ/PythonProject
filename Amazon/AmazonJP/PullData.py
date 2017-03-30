#!/usr/bin/env python
# -*- coding: utf-8 -*-


# 1 ----------------模块导入
import re
import datetime
from bs4 import BeautifulSoup
import http.cookiejar
import urllib.request, urllib.parse, urllib.error
import sys
import threading
import time
sys.path.append('..')
from Utils import *
from GenDescription import *
from GenWirelessDesc import *
from GenImage import *


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
# 模拟浏览器登录
values = {'email': 'wyjxjm@126.com', 'password': '324712', 'submit': 'Login'}
postdata = urllib.parse.urlencode(values).encode()
user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}
cookie_filename = 'cookie.txt'
cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)


# 3 ----------------数据获取
def pullData(html_url):
    println(u'\n\n打印获取数据------------------------------------------------')

    # 商品总信息列表
    product_info_list = []

    # 商品总信息字典
    # product_info_dict = {}

    # 所有图片链接列表
    product_image_list = []

    # 提取网页内容
    if 'html' in html_url:
        html_url = 'Htmls/' + html_url
        #html_url=r'D:\projects\amazon\3.htm'
        html_file = open(html_url, encoding='UTF-8')
    else:
        try:
            request = urllib.request.Request(html_url, postdata, headers)
            html_file = opener.open(request)
        except urllib.error.URLError as e:
            print(e.code, ':', e.reason)
        cookie.save(ignore_discard=True, ignore_expires=True)
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
    # product_info_dict['title'] = title
    product_info_list.append(title)
    println(u'宝贝名称: %s' % title)

    # 3.2 宝贝类目
    cid = 50018961
    # product_info_dict['cid'] = cid
    product_info_list.append(cid)
    println(u'宝贝类目: %d' % cid)

    # 3.3 店铺类目
    seller_cids = 50018961
    # product_info_dict['seller_cids'] = seller_cids
    product_info_list.append(seller_cids)
    println(u'店铺类目: %d' % seller_cids)

    # 3.4 淘宝新旧程度
    stuff_status = 1
    # product_info_dict['stuff_status'] = stuff_status
    product_info_list.append(stuff_status)
    println(u'新旧程度: %d' % stuff_status)

    # 3.5 省
    location_state = u'海外'
    # product_info_dict['location_state'] = location_state
    product_info_list.append(location_state)
    println(u'省: %s' % location_state)

    # 3.6 城市
    location_city = u'日本'
    # product_info_dict['location_city'] = location_city
    product_info_list.append(location_city)
    println(u'城市: %s' % location_city)

    # 3.7 出售方式
    item_type = 1
    # product_info_dict['item_type'] = item_type
    product_info_list.append(item_type)
    println(u'出售方式: %d' % item_type)

    # 3.8 宝贝价格
    # 原价
    print(u'src_price--原价: ')
    src_price = 0
    src_price_node = bs_obj.find('', {'id': 'priceblock_ourprice'})
    if src_price_node and len(src_price_node) > 0:
        src_price = int(src_price_node.get_text().replace('￥', '').replace(',', '').strip())
    println(src_price)

    # 配送费
    print(u'ship_price--配送费: ')
    ship_price = 500
    ship_price_node = bs_obj.find('', {'id': 'price-shipping-message'})
    if ship_price_node and len(ship_price_node) > 0:
        ship_price_text = ship_price_node.get_text().replace('\n', '').strip()
        if u'配送無料' in ship_price_text:
            if '¥' not in ship_price_text:
                ship_price = 0
    println(ship_price)

    # 商品详细
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


    # 价格计算
    i = 0
    weight_temp = str('1000000克')
    for items_Lable in detail_label_list:
        if (re.search(r".*重量.*", detail_label_list[i]) != None):
            weight_temp = detail_value_list[i]
            break
        i = i + 1
    if (re.search(r".*公斤.*", weight_temp) != None):
        weight = int(1000*float((weight_temp.replace(u'公斤', '').strip())))
    elif (re.search(r".*克.*", weight_temp) != None):
        weight = int(weight_temp.replace(u'克', '').strip())
    else:
        weight = 1000000
    if (weight + packet_weight) < 500:
        ems = 100
    else:
        ems = 100 + ((weight + packet_weight - 500) / 100) * 10
    price = round(((src_price + ship_price) / exchange_rate + (ems)) * (1 + profit_rate))
    # product_info_dict['price'] = price
    product_info_list.append(price)
    println(u'宝贝价格: %d' % price)

    # 3.9 加价幅度
    auction_increment = 0
    # product_info_dict['auction_increment'] = auction_increment
    product_info_list.append(auction_increment)
    println(u'加价幅度: %d' % auction_increment)

    # 3.10 宝贝数量
    num = 0
    num_node = bs_obj.find('', {'id': 'availability'})
    if num_node and len(num_node) > 0:
        num_text = num_node.get_text().replace('\n', '').strip()
        if (re.search(r".*在庫あり.*",num_text) != None):
            num = 50
        elif (re.search(r".*残り.*",num_text) != None):
            num = 5
        else:
            num = 0
    # product_info_dict['num'] = num
    product_info_list.append(num)
    println(u'宝贝数量: %d' % num)

    # 3.11 有效期
    #now = datetime.datetime.today() + datetime.timedelta(days=6)
    #valid_thru = now.strftime('%Y/%m/%d %H:%M')
    valid_thru = 7 #有效期是数字不是日期
    # product_info_dict['valid_thru'] = valid_thru
    product_info_list.append(valid_thru)
    println(u'有效期: %s' % valid_thru)

    # 3.12 运费承担
    freight_payer = 2
    # product_info_dict['freight_payer'] = freight_payer
    product_info_list.append(freight_payer)
    println(u'运费承担: %d' % freight_payer)

    # 3.13 平邮
    post_fee = 0
    # product_info_dict['post_fee'] = post_fee
    product_info_list.append(post_fee)
    println(u'平邮: %d' % post_fee)

    # 3.14 EMS
    ems_fee = 2
    # product_info_dict['ems_fee'] = ems_fee
    product_info_list.append(ems_fee)
    println(u'EMS: %d' % ems_fee)

    # 3.15 快递
    express_fee = 0
    # product_info_dict['express_fee'] = express_fee
    product_info_list.append(express_fee)
    println(u'快递: %d' % express_fee)

    # 3.16 发票
    has_invoice = 1
    # product_info_dict['has_invoice'] = has_invoice
    product_info_list.append(has_invoice)
    println(u'发票: %d' % has_invoice)

    # 3.17 保修
    has_warranty = 1
    # product_info_dict['has_warranty'] = has_warranty
    product_info_list.append(has_warranty)
    println(u'保修: %d' % has_warranty)

    # 3.18 放入仓库
    approve_status = 1
    # product_info_dict['approve_status'] = approve_status
    product_info_list.append(approve_status)
    println(u'放入仓库: %d' % approve_status)

    # 3.19 橱窗推荐
    has_showcase = 0
    # product_info_dict['has_showcase'] = has_showcase
    product_info_list.append(has_showcase)
    println(u'橱窗推荐: %d' % has_showcase)

    # 3.20 开始时间
    now = datetime.datetime.today()
    list_time = ''
    # product_info_dict['list_time'] = list_time
    product_info_list.append(list_time)
    println(u'开始时间: %s' % list_time)

    # 3.21 商品描述
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
        for feature_text in feature_node.find_all('span', {'class': 'a-list-item'}):
            if feature_text != '\n':
                feature = translate(feature_text.get_text().strip().replace('\n', '').replace('\'', '')
                                    .replace('[', '').replace(']', '').replace('【', '').replace('】', ''))
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
                image = image_text.get('src').replace('SS40', 'SL600')
                image_list.append(image)
                println(image)
    if len(image_list) == 0:
        println(u'无')
    else:
        product_image_list += image_list

    # product-description_feature商品描述1
    print(u'description_list--product-description_feature描述: ')
    delete_img_head_reg = re.compile("<img")
    delete_html_head_reg = re.compile("<[^>]*>")
    delete_n_reg = re.compile("\n*")
    search_http_reg = re.compile("src=[^>]*>")
    change_imagesize_reg = re.compile("__.*_")
    product_feature_div_description_list = []
    product_feature_div_node = bs_obj.find('div', id=re.compile(".*descriptionAndDetails.*"))
    if product_feature_div_node and len(product_feature_div_node) > 0:
        image_head_deleted_content_product = delete_img_head_reg.sub('', product_feature_div_node.prettify())
        html_head_deleted_content_product = delete_html_head_reg.sub('', image_head_deleted_content_product)\
            .replace(' ', '').strip('\n')
        content_list_product = delete_n_reg.split(html_head_deleted_content_product)
        for content_item_product in content_list_product:
            if re.search('src=', content_item_product) == None:
                content_temp_product = translate(content_item_product)
            else:
                pure_link_name_product = search_http_reg.search(content_temp_product).group()\
                    .strip("src=").strip("/>").strip('"')
                content_temp_product = change_imagesize_reg.sub('__SL600_', pure_link_name_product)
            product_feature_div_description_list.append(content_temp_product)
    if len(product_feature_div_description_list) == 0:
        println(u'无')
    else:
        println(product_feature_div_description_list)

    # aplus_feature_div商品描述2
    print(u'description_list--aplus_feature_div描述: ')
    aplus_feature_div_description_list = []
    aplus_feature_div_node = bs_obj.find('div', id=re.compile(".*aplus_feature_div.*"))
    if aplus_feature_div_node and len(aplus_feature_div_node) > 0:
        image_head_deleted_content = delete_img_head_reg.sub('', aplus_feature_div_node.prettify())
        html_head_deleted_content = delete_html_head_reg.sub('', image_head_deleted_content).replace(' ', '')\
            .strip('\n')
        content_list = delete_n_reg.split(html_head_deleted_content)
        for content_item in content_list:
            if re.search('src=', content_item) == None:
                content_temp = translate(content_item)
            else:
                pure_link_name = search_http_reg.search(content_item).group().strip("src=").strip("/>").strip('"')
                content_temp = change_imagesize_reg.sub('__SL600_', pure_link_name)
            aplus_feature_div_description_list.append(content_temp)
    if len(aplus_feature_div_description_list) == 0:
        println(u'无')
    else:
        println(aplus_feature_div_description_list)

    # 商品问答环节
    print(u'question_dict--商品问答环节: ')
    question_list = []
    question_node = bs_obj.find('', id=re.compile(".*ask-btf_feature_div.*"))
    if question_node and len(question_node) > 0:
        if len(question_list) == 0 or len(answer_list) == 0:
            html_head_deleted_content_question = delete_html_head_reg.sub('', question_node.prettify()).replace(' ', '').strip('\n')
            question_list = delete_n_reg.split(html_head_deleted_content_question)
    if len(question_list) == 0:
        println(u'无')
    else:
        println(question_list)

    # 客户评论
    print(u'comment_image_list--客户评论: ')
    comment_image_text_list = []
    comment_node = bs_obj.find('', id=re.compile(".*customer-reviews_feature_div.*"))
    if comment_node and len(comment_node) > 0:
        image_head_deleted_content_comment = delete_img_head_reg.sub('', comment_node.prettify())
        html_head_deleted_content_comment = delete_html_head_reg.sub('', image_head_deleted_content_comment)\
            .replace(' ', '').strip('\n')
        content_list_comment = delete_n_reg.split(html_head_deleted_content_comment)
        for content_item_comment in content_list_comment:
            if re.search('src=', content_item_comment) == None:
                content_temp_comment = translate(content_item_comment)
            else:
                pure_link_name_comment = search_http_reg.search(content_item_comment).group().strip("src=")\
                    .strip("/>").strip('"')
                content_temp_comment = change_imagesize_reg.sub('__SL600_', pure_link_name_comment)
            comment_image_text_list.append(content_temp_comment)
    if len(comment_image_text_list) == 0:
        println(u'无')
    else:
        println(comment_image_text_list)

    description = genDescription(feature_list, image_list, product_feature_div_description_list, aplus_feature_div_description_list, comment_image_text_list)
    # product_info_dict['description'] = description
    product_info_list.append(description)

    # 新图片下载与路径写入csv
    asin_number = bs_obj.find('', {'name': 'ASIN'})['value']
    thread = threading.Thread(target=genImage, name=str(asin_number), args=(product_image_list, str(asin_number)))
    thread.setDaemon(True)
    thread.start()
    # time.sleep(20)
    thread.join()

    # 3.22 宝贝属性
    cateProps = ''
    # product_info_dict['cateProps'] = cateProps
    product_info_list.append(cateProps)

    # 3.23 邮费模版ID
    postage_id = 5352276030
    # product_info_dict['postage_id'] = postage_id
    product_info_list.append(postage_id)

    # 3.24 会员打折
    has_discount = 0
    # product_info_dict['has_discount'] = has_discount
    product_info_list.append(has_discount)

    # 3.25 修改时间
    modified = list_time
    # product_info_dict['modified'] = modified
    product_info_list.append(modified)

    # 3.26 上传状态
    upload_fail_msg = ''
    # product_info_dict['upload_fail_msg'] = upload_fail_msg
    product_info_list.append(upload_fail_msg)

    # 3.27 图片状态
    picture_status = '1;1;1;1;1;'
    # product_info_dict['picture_status'] = picture_status
    product_info_list.append(picture_status)

    # 3.28 返点比例
    auction_point = 0
    # product_info_dict['auction_point'] = auction_point
    product_info_list.append(auction_point)

    # 3.29 新图片
    picture = ''
    new_picture_temp = '805567564a7cbdc' + str(asin_number) + 'i1' + ':1:i2:|;'
    for i in list(range(len(product_image_list))):
        if i < 10:
            i1 = '0' + str(i)
        else:
            i1 = str(i)
        i2 = str(i)
        picture += new_picture_temp.replace('i1', i1).replace('i2', i2)
    # product_info_dict['picture'] = picture
    product_info_list.append(picture)

    # 3.30 视频
    video = ''
    # product_info_dict['video'] = video
    product_info_list.append(video)

    # 3.31 销售属性组合
    skuProps = '197:50::1627207:-1001;137:50::1627207:-1002;'
    # product_info_dict['skuProps'] = skuProps
    product_info_list.append(skuProps)

    # 3.32 用户输入ID串
    inputPids = ''
    # product_info_dict['inputPids'] = inputPids
    product_info_list.append(inputPids)

    # 3.33 用户输入名-值对
    inputValues = ''
    # product_info_dict['inputValues'] = inputValues
    product_info_list.append(inputValues)

    # 3.34 商家编码
    outer_id = detail_value_list[detail_label_list.index(u'ASIN')]
    # product_info_dict['outer_id'] = outer_id
    product_info_list.append(outer_id)

    # 3.35 销售属性别名
    propAlias = ''
    # product_info_dict['propAlias'] = propAlias
    product_info_list.append(propAlias)

    # 3.36 代充类型
    auto_fill = ''
    # product_info_dict['auto_fill'] = auto_fill
    product_info_list.append(auto_fill)

    # 3.37 数字ID
    num_id = '543000000000'
    # product_info_dict['num_id'] = num_id
    product_info_list.append(num_id)

    # 3.38 本地ID
    local_cid = '-1'
    # product_info_dict['local_cid'] = local_cid
    product_info_list.append(local_cid)

    # 3.39 宝贝分类
    navigation_type = 2
    # product_info_dict['navigation_type'] = navigation_type
    product_info_list.append(navigation_type)

    # 3.40 用户名称
    user_name = 'scjmanbuman'
    # product_info_dict['user_name'] = user_name
    product_info_list.append(user_name)

    # 3.41 宝贝状态
    syncStatus = '1'
    # product_info_dict['syncStatus'] = syncStatus
    product_info_list.append(syncStatus)

    # 3.42 闪电发货
    is_lighting_consigment = '252'
    # product_info_dict['is_lighting_consigment'] = is_lighting_consigment
    product_info_list.append(is_lighting_consigment)

    # 3.43 新品
    is_xinpin = '248'
    # product_info_dict['is_xinpin'] = is_xinpin
    product_info_list.append(is_xinpin)

    # 3.44 食品专项
    foodparame = ''
    # product_info_dict['foodparame'] = foodparame
    product_info_list.append(foodparame)

    # 3.45 尺码库
    features = 'mysize_tp:0;sizeGroupId:;sizeGroupType:;tags:4674,32706,25282'  #
    # product_info_dict['features'] = features
    product_info_list.append(features)

    # 3.46 采购地
    buyareatype = '1'
    # product_info_dict['buyareatype'] = buyareatype
    product_info_list.append(buyareatype)

    # 3.47 库存类型
    global_stock_type = '2'
    # product_info_dict['global_stock_type'] = global_stock_type
    product_info_list.append(global_stock_type)

    # 3.48 国家地区
    global_stock_country = '日本'
    # product_info_dict['global_stock_country'] = global_stock_country
    product_info_list.append(global_stock_country)

    # 3.49 库存计数
    sub_stock_type = '1'
    # product_info_dict['sub_stock_type'] = sub_stock_type
    product_info_list.append(sub_stock_type)

    # 3.50 物流体积
    item_size = '0.000001'
    # product_info_dict['item_size'] = item_size
    product_info_list.append(item_size)

    # 3.51 物流重量
    item_weight = round(((weight + packet_weight)/1000),1)
    # product_info_dict['item_weight'] = item_weight
    product_info_list.append(item_weight)

    # 3.52 退换货承诺
    sell_promise = '0'
    # product_info_dict['sell_promise'] = sell_promise
    product_info_list.append(sell_promise)

    # 3.53 定制工具
    custom_design_flag = ''
    # product_info_dict['custom_design_flag'] = custom_design_flag
    product_info_list.append(custom_design_flag)

    # 3.54 无线详情
    wireless_desc = genWirelessDesc(title, feature_list, image_list, product_feature_div_description_list,
                                 aplus_feature_div_description_list, comment_image_text_list)
    # product_info_dict['wireless_desc'] = wireless_desc
    product_info_list.append(wireless_desc)

    # 3.55 商品条形码
    barcode = ''
    # product_info_dict['barcode'] = barcode
    product_info_list.append(barcode)

    # 3.56 sku 条形码
    sku_barcode = ''
    # product_info_dict['sku_barcode'] = sku_barcode
    product_info_list.append(sku_barcode)

    # 3.57 7天退货
    newprepay = '0'
    # product_info_dict['newprepay'] = newprepay
    product_info_list.append(newprepay)

    #3.58 宝贝卖点
    subtitle_temp=str()
    for text in feature_list:
        subtitle_temp += text
    subtitle = subtitle_temp[0:139]
    # product_info_dict['subtitle'] = subtitle
    product_info_list.append(subtitle)
    println(u'宝贝卖点: %s' % subtitle)

    # 3.59 属性值备注
    cpv_memo = ''
    # product_info_dict['cpv_memo'] = cpv_memo
    product_info_list.append(cpv_memo)

    # 3.60 自定义属性值
    input_custom_cpv = ''
    # product_info_dict['input_custom_cpv'] = input_custom_cpv
    product_info_list.append(input_custom_cpv)

    # 3.61 商品资质
    qualification = ''
    # product_info_dict['qualification'] = qualification
    product_info_list.append(qualification)

    # 3.62 增加商品资质
    add_qualification = '0'
    # product_info_dict['add_qualification'] = add_qualification
    product_info_list.append(add_qualification)

    # 3.63 关联线下服务
    o2o_bind_service = '0'
    # product_info_dict['o2o_bind_service'] = o2o_bind_service
    product_info_list.append(o2o_bind_service)

    # print(u'商品信息字典形式: ')
    # println(product_info_dict)
    print(u'商品信息列表形式: ')
    println(product_info_list)

    return product_info_list





