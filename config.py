#-*- coding: UTF-8 -*-
#针对查询 返回的记录数
query_return_numbers=20
#针对查询 返回的每条摘要长度
query_return_snipper_size=250
#针对某项查询 推荐的相似文档数目
recommand_numbers=3
#针对搜索词 推荐的相似主题数目
recommand_topic_numbers=10

#按块读取文件，块大小 :用于read_block() write_bloack(),针对只需读写一遍的大文件
buff_size=1024*1024*10
#将文件部分记录保存至内存，内存大小 ，内存中命中某项记录，直接从内存中取出记录，否则从磁盘读取记录，同时更新内存: 针对需多次读写的文件
cache_size=1024*1024*10
#爬取的网页数目
crawled_web_numbers=100000

#存储爬虫数据 文件名
#格式：doc_id#####title#####content#####url#####
#编码：utf-8
data_filename="_data.txt"
#存储爬取网页链接数据 文件名
#格式：url#####
#编码：utf-8
url_filename="_url.txt"
#存储网页倒排索引数据 文件名
#格式：word:doc_id#tf:doc_id#tf|
#编码：utf-8
inverted_index_filename="_data_inverted_index.txt"
#存储 文件名
#格式：word:word文档频率df:此项word在倒排索引文件中字节位置：此项word倒排索引长度
#注：起始位置为词项对应的以一个doc_id位置 绝对地址
#    所占字节数 从第一个doc_id存储位置至 最后一个tf存储位置止，而不是最后的'|' 绝对地址
#实例：  陈晓华:3:177112568:22|
#编码：utf-8
inverted_Dictionary_filename="_data_inverted_Dictionary.txt"
#存储网页倒排索引数据 文件名
#格式：doc_id:此项网页在爬取数据中字节位置：此项网页长度|
#注： 网页长度包括末尾的'#####'
#实例  77719:176500446:1723
#编码：utf-8
index_filename="_index.txt"
#存储与此项文档相似的文档id 文件名
#格式：doc_id:相似网页id：相似网页id|
#编码：utf-8
similar_filename="_similar.txt"
#存储停用词 文件名
#格式：停用词/n
#注意 文件名前无前缀
#编码：utf-8
stopword_filename="stopword.txt"
#存储训练好word2Vec 文件名
word2Vec_filename="vectors.bin"