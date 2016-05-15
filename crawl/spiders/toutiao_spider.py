#-*- coding: UTF-8 -*-
#scrapy crawl toutiao -o toutiao_items.json
#scrapy shell "http://toutiao.com/a6278566838045507841/"
import scrapy
#from ..items import toutiaoItem
import re


class toutiaoSpider(scrapy.spiders.Spider):
    name = "toutiao"#
    domains = "http://toutiao.com/"
    start_urls = [
        "http://toutiao.com/"
    ]
    links_dic={"http://toutiao.com/":"begin"}#访问的网页，以字典的形式实现
                                                 #目标网页：父网页
    length=1
    crawl_number=100                            #需要爬取网页的数目
    #file_object = open('data/toutiao_crawl_path.txt', 'w')          #保存爬取的链接和其父节点，便于分析爬取路径，从而分析质量
    has_write=False                                 #为保证在写文件结束后能够正常关闭文件
    def parse(self,response):
        #item =toutiaoItem()
        #item['keywords'] = response.xpath('//meta[@name="keywords"]/@content').extract()
        #item['title']=response.xpath('//div[@class="article-header"]/h1[@class="title"]').extract()
        #item['content']= response.xpath('//div[@class="article-content"]').extract()
        #item['link']=response.url
        #yield item

        links=response.xpath('//a[@ga_event="click_title_relevant"]/@href').extract() #提取头条具体某页新闻链接
        buff=response.xpath('//a[@ga_event="click_feed_newsimg"]/@href').extract()     #提取头条首页新闻链接
        for link in buff:
            links.append='http://toutiao.com'+link

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



