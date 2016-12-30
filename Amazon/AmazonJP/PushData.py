# -*- coding: utf-8 -*-


# 1----------------模块导入
import csv
import sys
sys.path.append('..')
from Utils import *


# 2 ----------------数据写入csv
def pushData(product_info_list):
    println(u'\n\n打印表格数据------------------------------------------------')

    item_file = open('Items.csv', 'a+', newline='')
    item_writer = csv.writer(item_file, dialect='excel')
    item_writer.writerow(product_info_list)
    item_file.close()

    item_file = open('Items.csv', 'r')
    item_reader = csv.reader(item_file)
    for item in item_reader:
        println(item)
    item_file.close()