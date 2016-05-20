#-*- coding: UTF-8 -*-
#测试
index_file=open("data/netease_data_inverted_index.txt",'r')
print index_file.read()[2597:2597+7]

index_file.seek(0,0)
index_file.seek(2597)
print index_file.tell()
print index_file.readline()
print index_file.tell()