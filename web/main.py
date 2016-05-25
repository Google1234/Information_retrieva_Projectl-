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
recommand=News_Recommend.CosineScore(path+config.inverted_Dictionary_filename,path+config.inverted_index_filename,config.buff_size,config.crawled_web_numbers)
#recommand=News_Recommend.FastCosineScore(filename[:-4]+'_index_Dictionary.txt',filename[:-4]+'_inverted_index.txt',buff_size,100000)
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
            topK=recommand.calculate(word_list,config.query_return_numbers)
            for k in topK:
                data = dict()
                title, content, url= id_index.get_data(k)
                data['id'] = k
                data['content'] = content.decode("utf-8")[:config.query_return_snipper_size]
                data['time'] = ''
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
            news['time'] = ''
            news['title'] = title.decode("utf-8")
            news['url'] = url.decode("utf-8")
        else:
            ID=''
            news = dict()
            news['title'] = "No Such News"
            news['time'] = ''
            news['content'] = "Oh No!"
            news['url'] = "#"
        return render.news(news)

if __name__ == "__main__":
	app = web.application(urls,globals())
	app.run()
