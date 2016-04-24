#-*- coding: UTF-8 -*-
#scrapy crawl netease -o items.json
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
    crawl_number=2000                            #需要爬取网页的数目
    file_object = open('dic.txt', 'w')          #保存爬取的链接和其父节点，便于分析爬取路径，从而分析质量
    has_write=False                                 #为保证在写文件结束后能够正常关闭文件
    def parse(self,response):
        item = neteaseItem()
        item['keywords'] = response.xpath('//head/meta[@name="keywords"]').extract()
        item['title']=response.xpath('//div[@class="post_content_main"]/h1').extract()
        item['content']=response.xpath('//div[@class="post_text"]/p').extract()
        item['link']=response.url
        yield item

        links=response.xpath('//a/@href').extract()
        for url in links:
            if re.match(self.domains,url):
                if self.links_dic.has_key(url)==False:
                    if self.length<self.crawl_number:
                        self.links_dic[url]=response.url
                        self.length+=1
                        #写爬取链接至txt文件
                        self.file_object.write(response.url)
                        self.file_object.write('\t')
                        self.file_object.write(url)
                        self.file_object.write('\n')
                        #
                        yield scrapy.Request(url, callback=self.parse)
        #结束写文件时需要关闭file
        if self.length>=self.crawl_number and self.has_write==False:
            self.file_object.close()
            self.has_write=True



