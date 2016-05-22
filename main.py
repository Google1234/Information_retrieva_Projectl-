#-*- coding: UTF-8 -*-
import inverted_files
import Dictionary
import News_Recommend

buff_size=1024*1024
output_record_size=40
filename="data/netease_data.txt"
inverted_files.make_inverted_index(filename,buff_size,output_record_size)


#加载存储的词典
cache_size=1024*1024
div=Dictionary.dictionary(filename[:-4]+"_index_Dictionary.txt",filename[:-4]+'_inverted_index.txt',cache_size)
print div.get_idfANDinvertedindex("概率")
