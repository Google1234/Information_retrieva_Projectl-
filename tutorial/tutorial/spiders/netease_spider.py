#-*- coding: UTF-8 -*-
import scrapy
from ..items import neteaseItem
import re
class neteaseSpider(scrapy.spiders.Spider):
    name = "netease"#网易
    allowed_domains = ["http://news.163.com/"]
    start_urls = [
        "http://news.163.com/"
    ]
    links_dic={start_urls[0]:0}#待访问网页序列，以字典的方式实现
    list=[]
    list.append(start_urls[0])
    index=0
    length=1
    flag=0

    def parse(self,response):
        #yield scrapy.Request(self.list[self.index], callback=self.parseUrl)
        yield scrapy.Request(self.list[self.index],self.parseUrl)
        '''
        while self.index<5:
            if self.links_dic[response.url]==0 and self.flag==0:

                yield scrapy.Request(self.list[self.index], callback=self.parseUrl)
                self.flag=1

            if self.links_dic[response.url]==2:
                self.index+=1
                yield scrapy.Request(self.list[self.index], callback=self.parseUrl)
        '''

    def parseUrl(self,response):
        print('ggggggggggggggggggg\n\n\n\n')
        self.links_dic[response.url]=2
        links=response.xpath('//a/@href').extract()
        for url in links:
            if re.match(self.allowed_domains[0],url):
                if self.links_dic.has_key(url)==False:
                    self.links_dic[url]=1
                    self.length+=1
                    self.list.append(url)
                    yield scrapy.Request(url, callback=self.parseNews)

    def parseNews(self,response):
        self.links_dic[response.url]=3
        item = neteaseItem()
        item['keywords'] = response.xpath('//head/meta[@name="keywords"]').extract()
        item['title']=response.xpath('//div[@class="post_content_main"]/h1').extract()
        item['content']=response.xpath('//div[@class="post_text"]/p').extract()
        item['link']=response.url
        yield item