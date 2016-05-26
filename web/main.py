#-*- coding: UTF-8 -*-
import os
import web
import sys
sys.path.append("..")
import News_Recommend
import similar_doc
import jieba
import config

path="../data/netease"
query=News_Recommend.CosineScore(path+config.inverted_Dictionary_filename,path+config.inverted_index_filename,config.buff_size,config.crawled_web_numbers)
recommand=News_Recommend.FastCosineScore(path+config.inverted_Dictionary_filename,path+config.inverted_index_filename,config.cache_size,path[:-7]+config.stopword_filename,config.crawled_web_numbers)
#recommand.get_from_file(path+config.similar_filename)
#query=News_Recommend.FastCosineScore(filename[:-4]+'_index_Dictionary.txt',filename[:-4]+'_inverted_index.txt',buff_size,100000)
id_index=similar_doc.doc_id_index(path+config.index_filename,path+config.data_filename,config.cache_size)
punct = set(u'''/+%#:!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')
Letters_and_numbers = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')


render = web.template.render('templates/')

urls=(
	"/","index",
	"/news","news"
)

app = web.application(urls,globals())
class index:
    def __init__(self):
        pass
    def GET(self):
        data=web.input()
        if data:
            searchword=data.searchword
        else:
            searchword=''
        news_list=list()
        if searchword:
            cut = jieba.cut_for_search(searchword)
            word_list = []
            for word in cut:
                if word not in punct and word not in Letters_and_numbers:
                    word_list.append(word.encode("utf-8"))
            topK=query.calculate(word_list,config.query_return_numbers)
            for k in topK:
                data = dict()
                title, content, url= id_index.get_data(k)
                data['id'] = k
                data['content'] = content.decode("utf-8")[:config.query_return_snipper_size]
                data['title']=title.decode("utf-8")
                data['url'] = url.decode("utf-8")
                news_list.append(data)
            del data,cut,word_list,word,topK,title,content,url
        return render.index(searchword,news_list)
class news:
    def __init__(self):
        pass
    def GET(self):
        data=web.input()
        if data:
            ID=data.id
            news = dict()
            title, content, url=id_index.get_data(int(ID))
            news['content'] = content.decode("utf-8")
            news['title'] = title.decode("utf-8")
            news['url'] = url.decode("utf-8")
            recomand=[]
            #在线方法
            cut = jieba.cut_for_search(content)
            word_list = []
            for word in cut:
                if word not in punct and word not in Letters_and_numbers:
                    # 计算文档间相似度，必须去停用词，否则太慢
                    if recommand.stopword.has_key(word.encode("utf-8")):
                        pass
                    else:
                        word_list.append(word.encode("utf-8"))
            topk= recommand.calculate(word_list, config.recommand_numbers, 10)
            for i in topk:#在线方法
            #for i in recommand.dic[int(ID)]:#离线方法
                if i !=int(ID):
                    title, content, url=id_index.get_data(i)
                    recomand.append([title.decode('utf-8'),content.decode('utf-8'),url.decode('utf-8')])
            news['recommand']=recomand
            del title,content,url,recomand
        else:
            ID=''
            news = dict()
            news['title'] = "No Such News"
            news['content'] = "Oh No!"
            news['url'] = "#"
            news['recommand']=[['','',''] for m in range(config.recommand_numbers)]
        return render.news(news)

if __name__ == "__main__":
	app = web.application(urls,globals())
	app.run()
