#-*- coding: UTF-8 -*-
import inverted_files
import Dictionary
import News_Recommend
import jieba
import similar_doc
import config

#part :爬取数据 并保存
#需要先cd 至 Information_retrleva_Project
#运行    :scrapy crawl netease
#在class neteaseSpider(scrapy.spiders.Spider)中可以修改 爬取的条数、保存的文件名

#part ：从原始爬取数据中 处理得到 倒排索引和词典
'''
buff_size=1024*1024*10
output_record_size=10000
filename="data/netease_data.txt"
inverted_files.make_inverted_index(filename,buff_size,output_record_size,100000)
#part :构建网页id索引
buff_size=1024*1024*10
similar_doc.establish_document_index("data/netease_data.txt",buff_size,"data/netease_index.txt")
'''

#part ：加载倒排索引和词典 相应查询或在线计算找到相似文档(可用于查询)
'''
buff_size=1024*1024*10
filename="data/netease_data.txt"
normal=News_Recommend.CosineScore(filename[:-4]+'_index_Dictionary.txt',filename[:-4]+'_inverted_index.txt',buff_size,100000)
#normal=News_Recommend.FastCosineScore(filename[:-4]+'_index_Dictionary.txt',filename[:-4]+'_inverted_index.txt',buff_size,100000)
topk=normal.calculate(["中国政法大学","研究员"])
cache_size=1024*1024*10
id_index=similar_doc.doc_id_index("data/netease_index.txt",filename,cache_size)
for i in topk:
    title,content,url=id_index.get_data(i)
    print title.decode("utf-8"),content.decode("utf-8"),url
'''

#part ：加载倒排索引和词典 通过读取文件找到找到相似文档(可用于快速相似新闻推荐)
'''
path="data/netease_"
buff_size=1024*1024*10
cache_size=1024*1024*10
s=similar_doc.similar(path+"index.txt",path+"data.txt",path+"data_index_Dictionary.txt",path+"data_inverted_index.txt",buff_size)
s.get_from_file(path+"similar.txt")
topk=s.dic[2]
id_index=similar_doc.doc_id_index("data/netease_index.txt",path+"data.txt",cache_size)
for i in topk:
    title,content,url=id_index.get_data(i)
    print title.decode("utf-8"),content.decode("utf-8"),url
'''

#part :保存相似的文档至文件
'''
path="data/netease"
s=similar_doc.similar(path+config.index_filename,path+config.data_filename,path+config.inverted_Dictionary_filename,path+config.inverted_index_filename,config.buff_size)
s.write_to_file(config.crawled_web_numbers,path+config.similar_filename)
'''


