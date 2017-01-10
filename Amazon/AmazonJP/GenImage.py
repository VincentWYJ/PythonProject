# -*- coding: utf-8 -*-


# 1 ----------------模块导入
import os
import shutil
import urllib.request


dir_path = 'Items'
start_number = dir_path+'/805567564a7cbdc692664733adf'
end_number = 10000
format = '.tbi'


# 2 ----------------生成tbi格式图片
def genImage(imageLink_list):
    # 2.1 清空目录
    # 如果不存在则新建，存在则删除所有内部已经存在的文件
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        # shutil.rmtree(dir_path) # 删除文件夹

    # 2.2 下载图片
    i = 0
    for link in imageLink_list:
        urllib.request.urlretrieve(link, start_number+str(end_number+i)+format)  # 下载图片
        i += 1

# 3 ----------------方法测试
# genImage(None)