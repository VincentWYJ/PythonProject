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

html_url = 'https://www.amazon.co.jp/%E8%B6%85%E9%9F%B3%E6%B3%A2%E5%BC%8F%E3%82%A2%E3%83%AD%E3%83%9E%E5%8A%A0%E6%B9%BF%E5%99%A8-%E3%82%BF%E3%83%B3%E3%82%AF%E5%AE%B9%E9%87%8F3-3L-SHIZUKU-%E3%82%BF%E3%83%83%E3%83%81%E3%83%91%E3%83%8D%E3%83%AB-OFF%E3%82%BF%E3%82%A4%E3%83%9E%E3%83%BC-AHD-015-WH/dp/B00XVHDM9K/ref=gbph_img_m-3_53ab_2ff992b3?smid=AN1VRQENFRJN5&pf_rd_p=bd811fff-5818-433d-b6e5-5bdce99353ab&pf_rd_s=merchandised-search-3&pf_rd_t=101&pf_rd_i=3895761&pf_rd_m=AN1VRQENFRJN5&pf_rd_r=N709N6T86ZPPZFKNT69B'
# 提取网页内容
if 'html' in html_url:
    html_url = 'Htmls/' + html_url
    html_file = open(html_url, encoding='UTF-8')
else:
    try:
        request = urllib.request.Request(html_url, postdata, headers)
        html_file = opener.open(request)
    except urllib.error.URLError as e:
        print(e.code, ':', e.reason)
    cookie.save(ignore_discard=True, ignore_expires=True)

bs_obj = BeautifulSoup(html_file.read(), 'html.parser')

detail_node = bs_obj.find('', {'id': 'detail_bullets_id'})
detail_label_list = []
detail_value_list = []
if detail_node and len(detail_node) > 0:
    for text in detail_node.find_all('li'):
        if text != '\n':
            text = translate(text.get_text().strip().replace('\n', ''))
            index = text.find('：')
            detail_label_list.append(text[0:index])
            detail_value_list.append(text[index+1:])
if len(detail_label_list) == 0 or len(detail_value_list) == 0:
    println('无')
else:
    for i in list(range(len(detail_label_list))):
        println(detail_label_list[i]+': '+detail_value_list[i])







