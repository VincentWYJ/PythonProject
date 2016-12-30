# -*- coding: utf-8 -*-


# 1 ----------------模块导入
import xlrd
import sys
sys.path.append('..')


# 2 ----------------返回html list
def pullHtml():
    xlsx_file = xlrd.open_workbook('Htmls/Htmls.xlsx')
    table = xlsx_file.sheet_by_name('Amazon')
    html_list = table.col_values(0)

    print(u'本地html列表: ')
    print(html_list)

    return html_list

# 2.1 方法测试
# html_list = pullHtml()