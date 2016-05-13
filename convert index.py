#-*- coding: UTF-8 -*-
import jieba
import re


f=open("tutorial/netease_data.txt",'r')
buff_size=1024*10
page_part_pointer=0
last_buff=''
while True:
   a=f.read(buff_size)
   if a=='':
       break
   else:
        a=last_buff+a
        i=len(last_buff)
        del last_buff
        last_i=0
        while i<len(a):
            if a[i]=='#':
                if a[i:i+5]=='#####':
                    if page_part_pointer%4==0:#保存 当前网页编号
                        page_id=a[last_i:i]
                        print page_id
                    if page_part_pointer%4==2:#保存 当前网页内容
                        page_content=a[last_i:i]
                        print page_content
                    i+=5
                    last_i=i
                    page_part_pointer+=1
            else:
                i+=1
        last_buff=a[last_i:i]
        del a
