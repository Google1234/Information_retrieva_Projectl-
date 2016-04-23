#-*- coding: UTF-8 -*-
import scrapy
from ..items import neteaseItem
import re
class neteaseSpider(scrapy.spiders.Spider):
    name = "netease"#网易
    domains = "http://news.163.com/"
    start_urls = [
        "http://news.163.com/"
    ]
    links_dic={"http://news.163.com/":"begin"}#访问的网页，以字典的形式实现
                                                 #目标网页：父网页
    length=1

    def parse(self,response):
        item = neteaseItem()
        item['keywords'] = response.xpath('//head/meta[@name="keywords"]').extract()
        item['title']=response.xpath('//div[@class="post_content_main"]/h1').extract()
        item['content']=response.xpath('//div[@class="post_text"]/p').extract()
        item['link']=response.url
        yield item

        if self.length<100:
            links=response.xpath('//a/@href').extract()
            for url in links:
                if re.match(self.domains,url):
                    if self.links_dic.has_key(url)==False:
                        self.links_dic[url]=response.url
                        self.length+=1
                        yield scrapy.Request(url, callback=self.parse)



