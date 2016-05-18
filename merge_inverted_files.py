#-*- coding: UTF-8 -*-
import os

'''
token:word=None page_id=[] tf=[]
'''
class read_block:
    def __init__(self,buff_size,filename):
        self.size=buff_size
        self.filename=open(filename,'r')
        self.buff=self.filename.read(self.size)
        self.pointer=0
        if  ord(self.buff[0])==0xEF and  ord(self.buff[1])==0xBB and ord(self.buff[2])==0xbf : #####解决BOM问题
            self.last_pointer=3
        else:
            self.last_pointer=0
    def read(self):
        if self.last_pointer==0:
            print "Error! :self.size is too small !self.buff is full,can not load new data!"
        a=self.buff[self.last_pointer:]+self.filename.read(self.last_pointer)
        del self.buff
        self.buff=a
        self.pointer-=self.last_pointer
        self.last_pointer=0

    def pop_token(self):
        while True:#word
            if self.pointer==self.size:
                self.read()
            if self.pointer==len(self.buff):
                return '','','' #表示文档读完
            if self.buff[self.pointer]==':':
                break
            self.pointer+=1
        word=self.buff[self.last_pointer:self.pointer]
        self.last_pointer=self.pointer+1

        doc_id=[]
        tf=[]
        while True:
            while True:#page
                if self.pointer==self.size:
                    self.read()
                if self.buff[self.pointer]=='#':
                    break
                self.pointer+=1
            doc_id.append(self.buff[self.last_pointer:self.pointer])
            self.last_pointer=self.pointer+1
            while True:#tf
                if self.pointer==self.size:
                    self.read()
                if self.buff[self.pointer]=='\n':#要求最后一项纪录必须以\n结尾
                    tf.append(self.buff[self.last_pointer:self.pointer])
                    self.last_pointer=self.pointer+1
                    return word,doc_id,tf
                if self.buff[self.pointer]==':':
                    break
                self.pointer+=1
            tf.append(self.buff[self.last_pointer:self.pointer])
            self.last_pointer=self.pointer+1
    def pop_rest(self):
        a=self.buff[self.last_pointer:]+self.filename.read(self.last_pointer)
        del self.buff
        self.buff=a
        self.pointer=self.last_pointer=self.size
        return self.buff
    def close(self):
        self.filename.close()
        del self.pointer,self.last_pointer,self.size,self.buff

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


def sort_fie(name_list,buff_size,datapath):
    if len(name_list)<=1:
        return name_list[0]
    else :
        left=name_list[:len(name_list)/2]
        right=name_list[len(name_list)/2:]
        left_file=sort_fie(left,buff_size,datapath)
        right_file=sort_fie(right,buff_size,datapath)
        '''
        merge 部分：
       '''
        read_block1=read_block(buff_size,datapath+left_file+'.txt')
        read_block2=read_block(buff_size,datapath+right_file+'.txt')
        write_block1=write_block(buff_size,datapath+left_file+'+'+right_file+'.txt')
        word1,doc1,tf1=read_block1.pop_token()
        word2,doc2,tf2=read_block2.pop_token()
        while True:
            if word1>word2:
                write_block1.push(word2)
                for i in range(len(doc2)):
                    write_block1.push(':'+doc2[i]+'#'+tf2[i])
                write_block1.push('\n')
                del word2,doc2,tf2
                word2,doc2,tf2=read_block2.pop_token()
                if word2=='':
                    break
            if word1<word2:
                write_block1.push(word1)
                for i in range(len(doc1)):
                    write_block1.push(':'+doc1[i]+'#'+tf1[i])
                write_block1.push('\n')
                del word1,doc1,tf1
                word1,doc1,tf1=read_block1.pop_token()
                if word1=='':
                    break
            if word1==word2:
                write_block1.push(word2)
                i=j=0
                while i<len(doc1) and  j<len(doc2):
                    print word1,doc1[i],doc2[j]
                    if int(doc1[i])<int(doc2[j]):
                        write_block1.push(':'+doc1[i]+'#'+tf1[i])
                        i+=1
                    else:
                        if int(doc1[i])>int(doc2[j]):
                            write_block1.push(':'+doc2[j]+'#'+tf2[j])
                            j+=1
                        else:
                            write_block1.push(':'+doc2[j]+'#'+str(int(tf1[i])+int(tf2[j])))
                            i+=1
                            j+=1
                if i==len(doc1):
                    while j<len(doc2):
                        write_block1.push(':'+doc2[j]+'#'+tf2[j])
                        j+=1
                if j==len(doc2):
                    while i<len(doc1):
                        write_block1.push(':'+doc1[i]+'#'+tf1[i])
                        i+=1
                write_block1.push('\n')
                del word1,doc1,tf1,word2,doc2,tf2
                word1,doc1,tf1=read_block1.pop_token()
                word2,doc2,tf2=read_block2.pop_token()
                if word1=='':
                    break
                if word2=='':
                    break
        if word1=='':
            write_block1.push(word2)
            for i in range(len(doc2)):
                write_block1.push(':'+doc2[i]+'#'+tf2[i])
            write_block1.push('\n')
            del word2,doc2,tf2
            while True:
                block=read_block2.pop_rest()
                if block=='':
                    break
                write_block1.push(block)
                del block
        else :
            if word2=='':
                write_block1.push(word1)
                for i in range(len(doc1)):
                    write_block1.push(':'+doc1[i]+'#'+tf1[i])
                write_block1.push('\n')
                del word1,doc1,tf1
                while True:
                    block=read_block1.pop_rest()
                    if block=='':
                        break
                    write_block1.push(block)
                    del block
        write_block1.close()
        read_block1.close()
        read_block2.close()
        del write_block1,read_block1,read_block2
        return left_file+'+'+right_file

datapath='data/invert_index_test_'
buff_size=1024*1024
sort_fie([str(i) for i in range(1,3)],buff_size,datapath)
