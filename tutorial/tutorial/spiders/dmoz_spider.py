#! /usr/bin/env python
#coding=utf-8
from scrapy.selector import Selector
from scrapy.http import Request
import re,os
from bs4 import BeautifulSoup
from scrapy.spider import Spider
import urllib2,thread
#处理编码问题
import sys
reload(sys)
sys.setdefaultencoding('gb18030')
#flag的作用是保证第一次爬取的时候不进行单个新闻页面内容的爬取
flag=1
#projectpath='C:\\Python27\\pythonproject\\fuck\\'
projectpath='C:\\Python\\Information_retrieva_Projectl-\\tutorial\\'

def loop(*response):
        sel = Selector(response[0])
        #get title
        title = sel.xpath('//h1/text()').extract()
        #get pages
        pages=sel.xpath('//div[@id="artibody"]//p/text()').extract()
        #get chanel_id & comment_id
        s=sel.xpath('//meta[@name="comment"]').extract()
        #comment_id = channel[index+3:index+15]
        index2=len(response[0].url)
        news_id=response[0].url[index2-14:index2-6]
        comment_id='31-1-'+news_id
        #评论内容都在这个list中
        cmntlist=[]
        page=1
        #含有新闻url,标题,内容,评论的文件
        file2=None
        #该变量的作用是当某新闻下存在非手机用户评论时置为False
        is_all_tel=True
        while((page==1) or (cmntlist != [])):
            tel_count=0 #each page tel_user_count
            #提取到的评论url
            url="http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=cj&newsid="+str(comment_id)+"&group=0&compress=1&ie=gbk&oe=gbk&page="+str(page)+"&page_size=100"
            url_contain=urllib2.urlopen(url).read()
            b='={'
            after = url_contain[url_contain.index(b)+len(b)-1:]
            #字符串中的None对应python中的null，不然执行eval时会出错
            after=after.replace('null','None')
            #转换为字典变量text
            text=eval(after)
            if 'cmntlist' in text['result']:
                cmntlist=text['result']['cmntlist']
            else:
                cmntlist=[]
            if cmntlist != [] and (page==1):
                filename=str(comment_id)+'.txt'
                path=projectpath+'stock\\' +filename
                file2=open(path,'a+')
                news_content=str('')
                for p in pages:
                    news_content=news_content+p+'\n'
                item="<url>"+response[0].url+"</url>"+'\n\n'+"<title>"+str(title[0])+"</title>\n\n"+"<content>\n"+str(news_content)+"</content>\n\n<comment>\n"
                file2.write(item)
            if cmntlist != []:
                content=''
                for status_dic in cmntlist:
                    if status_dic['uid']!='0':
                        is_all_tel=False
                        #这一句视编码情况而定，在这里去掉decode和encode也行
                        s=status_dic['content'].decode('UTF-8').encode('GBK')
                        #见另一篇博客“三张图”
                        s=s.replace("'""'",'"')
                        s=s.replace("\n",'')
                        s1="u'"+s+"'"
                        try:
                            ss=eval(s1)
                        except:
                            try:
                                s1='u"'+s+'"'
                                ss=eval(s1)
                            except:
                                return
                        content=content+status_dic['time']+'\t'+status_dic['uid']+'\t'+ss+'\n'
                    #当属于手机用户时
                    else:
                        tel_count=tel_count+1
                #当一个page下不都是手机用户时，这里也可以用is_all_tel进行判断，一种是用开关的方式，一种是统计的方式
                #算了不改了
                if tel_count!=len(cmntlist):
                    file2.write(content)
            page=page+1
        #while loop end here
        if file2!=None:
            #当都是手机用户时，移除文件，否则写入"</comment>"到文件尾
            if is_all_tel:
                file2.close()
                try:
                    os.remove(file2.name)
                except WindowsError:
                    pass
            else:
                file2.write("</comment>")
                file2.close()
class DmozSpider(Spider):
    name = "stock"
    allowed_domains = ["sina.com.cn"]
    #在本程序中，start_urls并不重要，因为并没有解析
    start_urls = [
        "http://news.sina.com.cn/"
    ]
    global projectpath
    if os.path.exists(projectpath+'stock'):
        pass
    else:
        os.mkdir(projectpath+'stock')
    def parse(self, response):
        #这个scrapy.selector.Selector是个不错的处理字符串的类，python对编码很严格，它却处理得很好
        #在做这个爬虫的时候，碰到很多奇奇怪怪的编码问题，主要是中文，试过很多既有的类，BeautifulSoup处理得也不是很好
        sel = Selector(response)
        global flag
        if(flag==1):
            flag=2
            page=1
            while page<260:
                url="http://roll.finance.sina.com.cn/finance/zq1/index_"
                url=url+str(page)+".shtml"
                #伪装为浏览器
                user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
                headers = { 'User-Agent' : user_agent }
                req = urllib2.Request(url, headers=headers)
                response = urllib2.urlopen(req)
                url_contain = response.read()
                #利用BeautifulSoup进行文档解析
                soup = BeautifulSoup(url_contain)
                params = soup.findAll('div',{'class':'listBlk'})
                if os.path.exists(projectpath+'stock\\'+'link'):
                     pass
                else:
                     os.mkdir(projectpath+'stock\\'+'link')
                filename='link.txt'
                path=projectpath+'stock\\link\\' + filename
                filelink=open(path,'a+')
                for params_item in params:
                    persons = params_item.findAll('li')
                    for item in persons:
                        href=item.find('a')
                        mil_link= href.get('href')
                        filelink.write(str(mil_link)+'\n')
                        #递归调用parse,传入新的爬取url
                        yield Request(mil_link, callback=self.parse)
                page=page+1
        #对单个新闻页面新建线程进行爬取
        if flag!=1:
            if (response.status != 404) and (response.status != 502):
                thread.start_new_thread(loop,(response,))