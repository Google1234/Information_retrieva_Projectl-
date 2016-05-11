#-*- coding: UTF-8 -*-
#scrapy crawl netease -o netease.json
import scrapy
from ..items import neteaseItem
import re
import json

class neteaseSpider(scrapy.spiders.Spider):
    name = "netease"#网易
    domains = "http://news.163.com/"
    reject=["http://news.163.com/photoset/","http://news.163.com/photo/"] #实际测试中爬取10万条，有1万条左右都是只有图片，没有文字
    start_urls = [
        "http://news.163.com/"
    ]
    links_dic={"http://news.163.com/":"begin"}#访问的网页，以字典的形式实现
                                                 #目标网页：父网页
    id=1
    crawl_number=50                            #需要爬取网页的数目
    #min_length=10                               #网页文本大小阈值，小于阈值，不保存至txt
    file_object = open('netease_crawl_path.txt', 'w')          #保存爬取的链接和其父节点，便于分析爬取路径，从而分析质量
    data_file = open('netease_data.txt', 'w')
    dict_file = open('dict.txt', 'w')
    has_write=False                                 #为保证在写文件结束后能够正常关闭文件
    def parse(self,response):
        #keyword=response.xpath('//head/meta[@name="keywords"]/@content').extract()
        title=response.xpath('//div[@class="post_content_main"]/h1/text()').extract()
        content=response.xpath('//div[@class="post_text"]/p/text()').extract()
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

        #写爬取内容到txt
        if title and content:
            self.data_file.write(str(self.id))
            self.data_file.write('#####')
            for i in range(len(title)):
                self.data_file.write(title[i].encode('utf-8'))
            self.data_file.write('#####')
            for i in range(len(content)):
                self.data_file.write(content[i].encode('utf-8'))
            self.data_file.write('#####')
            self.data_file.write(link)
            self.data_file.write('#####')
            self.id+=1
            #写链接到txt
            self.dict_file.write(link)
            self.dict_file.write('\n')


        links=response.xpath('//a/@href').extract()
        for url in links:
            if re.match(self.domains,url):
                if self.links_dic.has_key(url)==False:
                    if self.id<self.crawl_number:
                        self.links_dic[url]=response.url
                        #写爬取链接至txt文件
                        self.file_object.write(response.url)
                        self.file_object.write('\t')
                        self.file_object.write(url)
                        self.file_object.write('\n')
                        #self.crawl_count+=1
                        yield scrapy.Request(url, callback=self.parse)
        #结束写文件时需要关闭file
        if self.id>=self.crawl_number and self.has_write==False:
            self.file_object.close()
            self.data_file.close()
            self.dict_file.close()
            self.has_write=True



