#-*- coding: UTF-8 -*-
#scrapy crawl netease
import scrapy
import re

class write_block:
    def __init__(self,buff_size,filename):
        self.remain=self.size=buff_size
        self.filename=filename
        file=open(self.filename,'w')
        file.close()
        self.buff=''
    def push(self,content):
        if len(content)>self.remain:
            self.buff+=content[:self.remain+1]
            file=open(self.filename,'a')
            file.write(self.buff)
            file.close()
            del self.buff
            self.buff=''
            self.buff+=content[self.remain+1:]
            self.remain=self.size -(len(content)-self.remain)
        else:
            self.buff+=content
            self.remain-=len(content)
    def close(self):
        file=open(self.filename,'a')
        file.write(self.buff)
        file.close()
        del self.buff
        self.buff=''
        self.remain=self.size

class neteaseSpider(scrapy.spiders.Spider):
    crawl_number=100000                          #需要爬取网页的数目
    write_data_file='data/netease_data.txt'
    write_crawled_weburl_file='data/netease_dict.txt'
    write_buff_size=1024*1024*10
    name = "netease"#网易
    domains = "http://news.163.com/"
    reject=["http://news.163.com/photoset/","http://news.163.com/photo/","http://news.163.com/editor","http://news.163.com/photoview/"] #实际测试中爬取10万条，有1万条左右都是只有图片，没有文字
    start_urls = [
        "http://news.163.com/"
    ]
    links_dic={"http://news.163.com/":"begin"}#目标网页：父网页 访问的网页，以字典的形式实现
    #file_object = open('netease_crawl_path.txt', 'w')          #保存爬取的链接和其父节点，便于分析爬取路径，从而分析质量
    #file_object.close()

    write_block_data=write_block(write_buff_size,write_data_file)
    write_block_crawlwd_weburl=write_block(write_buff_size,write_crawled_weburl_file)
    lock=False                                      #写文件锁
    has_terminated=False                            #为保证在写文件结束后能够正常关闭文件
    web_id=1
    def parse(self,response):
        if self.web_id>self.crawl_number:
            if self.has_terminated==False:
                self.write_block_data.close()
                self.write_block_crawlwd_weburl.close()
                del self.write_block_crawlwd_weburl,self.write_block_data
                self.has_terminated==True
        else:
            #keyword=response.xpath('//head/meta[@name="keywords"]/@content').extract()
            title=response.xpath('//head/title/text()').extract()
            content=response.xpath('//div/p/text()').extract()
            link=response.url
            if title and content:
                while(self.lock==True):
                    pass
                self.lock=True
                #写爬取内容到buff
                self.write_block_data.push(str(self.web_id)+'#####')
                for i in range(len(title)):
                    self.write_block_data.push(title[i].encode('utf-8'))
                self.write_block_data.push('#####')
                for i in range(len(content)):
                    self.write_block_data.push(content[i].encode('utf-8'))
                self.write_block_data.push('#####')
                self.write_block_data.push(link+'#####')
                #写爬取的链接
                self.write_block_crawlwd_weburl.push(link+'#####')
                self.web_id+=1
                self.lock=False

                links=response.xpath('//a/@href').extract()
                for url in links:
                    if re.match(self.domains,url):
                        if re.match(self.reject[0],url)==None and re.match(self.reject[1],url)==None and re.match(self.reject[2],url)==None and re.match(self.reject[3],url)==None:#不追踪reject中存储的网页链接
                            if self.links_dic.has_key(url)==False:
                                self.links_dic[url]=response.url
                                yield scrapy.Request(url)