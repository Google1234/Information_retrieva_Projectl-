#-*- coding: UTF-8 -*-
import inverted_files
import Dictionary
import News_Recommend
import jieba

buff_size=1024*1024
output_record_size=40
filename="data/netease_data.txt"

#part ：从原始爬取数据中 处理得到 倒排索引和词典
#inverted_files.make_inverted_index(filename,buff_size,output_record_size,400)

#part ：加载倒排索引和词典 相应查询或找到相似文档
#normal=News_Recommend.CosineScore(filename[:-4]+'_index_Dictionary.txt',filename[:-4]+'_inverted_index.txt',1024*1024,400)
normal=News_Recommend.FastCosineScore(filename[:-4]+'_index_Dictionary.txt',filename[:-4]+'_inverted_index.txt',1024*1024,400)
print normal.calculate(["郑过州","高新区"])