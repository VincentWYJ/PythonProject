# -*- coding: utf-8 -*-

import os
import http.cookiejar
from lxml import etree
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import xlrd


## 从Excel读取网址
# 获取所有数据
address_data = xlrd.open_workbook('../Excel/WebAddress.xlsx')
# 获取表Amazon数据
table_amazon = address_data.sheet_by_name('Amazon')
# 获取第一行数据——AmazonJP的登录与某一产品网址
address_jp =  table_amazon.row_values(0)

## 网站登录操作
login_url = address_jp[1]
values = {'email': 'wyjxjm@126.com', 'password': '324712', 'submit': 'Login'}
postdata = urllib.parse.urlencode(values).encode()
user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}

cookie_filename = 'cookie.txt'
cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
request = urllib.request.Request(login_url, postdata, headers)

try:
    response = opener.open(request)
    page = response.read().decode()
except urllib.error.URLError as e:
    print(e.code, ':', e.reason)
    
cookie.save(ignore_discard = True, ignore_expires = True)

print("Cookie info: ")
for item in cookie:
    print('Name = ' + item.name)
    print('Value = ' + item.value)


## 数据获取操作
get_url = address_jp[2]
get_request = urllib.request.Request(get_url, headers=headers)
get_response = opener.open(get_request)

bsobj = BeautifulSoup(get_response.read().decode(), "html.parser")

print("\nProduct info: ")
for el in bsobj.find_all("span", {"id": "productTitle"}):
    print(el.get_text())
