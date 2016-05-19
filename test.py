#-*- coding: UTF-8 -*-
import Dictionary

#Dictionary.establish_ditionary("data/netease_data1.txt",1024*1024,"data/netease_Dictionary.txt")
a=Dictionary.dictionary("data/netease_Dictionary.txt","data/netease_data1.txt",1024*1000)
print  a.get_idfANDinvertedindex("一百二十")