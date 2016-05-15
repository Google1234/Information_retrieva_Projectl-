#-*- coding: UTF-8 -*-
#scrapy crawl netease
import scrapy
import re


class neteaseSpider(scrapy.spiders.Spider):
    name = "netease"#网易
    domains = "http://news.163.com/"
    reject=["http://news.163.com/photoset/","http://news.163.com/photo/","http://news.163.com/editor","http://news.163.com/photoview/"] #实际测试中爬取10万条，有1万条左右都是只有图片，没有文字
    start_urls = [
        "http://news.163.com/"
    ]
    links_dic={"http://news.163.com/":"begin"}#访问的网页，以字典的形式实现
                                                 #目标网页：父网页
    id=1
    crawl_number=100000                           #需要爬取网页的数目
    #file_object = open('netease_crawl_path.txt', 'w')          #保存爬取的链接和其父节点，便于分析爬取路径，从而分析质量
    #file_object.close()
    data_file = open('data/netease_data.txt', 'w')
    data_file.close()
    dict_file = open('data/netease_dict.txt', 'w')
    dict_file.close()
    buff=[]
    buff_link=[]
    lock=False                                      #写文件锁
    has_write=False                                 #为保证在写文件结束后能够正常关闭文件
    def parse(self,response):
        #keyword=response.xpath('//head/meta[@name="keywords"]/@content').extract()
        title=response.xpath('//head/title/text()').extract()
        content=response.xpath('//div/p/text()').extract()
        link=response.url
        #存 json文件
        '''
        item = neteaseItem()
        #item['keywords'] = keyword
        item['title']=title
        item['content']=content
        item['link']=link
        yield item
        '''
        while(self.lock==True):
            pass
        #写爬取内容到buff
        if title and content:
            while(self.lock==True):
                pass
            self.buff.append(str(self.id))
            self.buff.append('#####')
            for i in range(len(title)):
                self.buff.append(title[i].encode('utf-8'))
            self.buff.append('#####')
            for i in range(len(content)):
                self.buff.append(content[i].encode('utf-8'))
            self.buff.append('#####')
            self.buff.append(link)
            self.buff.append('#####\n')
            self.buff_link.append(link)
            self.buff_link.append('\n')
            self.id+=1
        if self.id%100==0:  #防止内存溢出，若干次写一次文件
            self.lock=True
            data_file = open('data/netease_data.txt', 'a')
            for i in range(len(self.buff)):
                data_file.write(self.buff[i])
            data_file.close()
            dict_file = open('data/netease_dict.txt', 'a')
            for i in range(len(self.buff_link)):
                dict_file.write(self.buff_link[i])
            dict_file.close()
            del self.buff[:]
            del self.buff_link[:]
            self.lock=False

        links=response.xpath('//a/@href').extract()
        for url in links:
            if re.match(self.domains,url):
                if re.match(self.reject[0],url)==None and re.match(self.reject[1],url)==None and re.match(self.reject[2],url)==None and re.match(self.reject[3],url)==None:#不追踪reject中存储的网页链接
                    if self.links_dic.has_key(url)==False:
                        if self.id<self.crawl_number:
                            self.links_dic[url]=response.url
                            #self.crawl_count+=1
                            yield scrapy.Request(url, callback=self.parse)
