#-*- coding: UTF-8 -*-
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
        self.base_pointer=0
    def read(self):
        if self.last_pointer==0:
            print "Error! :self.size is too small !self.buff is full,can not load new data!"
        a=self.buff[self.last_pointer:]+self.filename.read(self.last_pointer)
        del self.buff
        self.buff=a
        self.pointer-=self.last_pointer
        self.base_pointer+=self.last_pointer
        self.base_offset-=self.last_pointer
        self.last_pointer=0
    def pop_token(self):
        '''
        返回 词项倒排记录相关值
        :return: word_id   文档号
                  pointer    指针              数值型
                  length  包括末尾的'#####'    数值型
        '''
        self.base_offset=self.last_pointer
        while True:#doc_id
            if self.pointer==self.size:
                self.read()
            if self.pointer==len(self.buff):
                return -1,0,0 #表示文档读完
            if self.buff[self.pointer:self.pointer+5]=='#####':
                break
            self.pointer+=1
        doc_id=self.buff[self.last_pointer:self.pointer]
        self.last_pointer=self.pointer+5
        self.pointer+=5
        while True:#title
            if self.pointer==self.size:
                self.read()
            if self.pointer==len(self.buff):
                return -1,0,0 #表示文档读完
            if self.buff[self.pointer:self.pointer+5]=='#####':
                break
            self.pointer+=1
        #title=self.buff[self.last_pointer:self.pointer]
        self.last_pointer=self.pointer+5
        self.pointer+=5
        while True:#content
            if self.pointer==self.size:
                self.read()
            if self.pointer==len(self.buff):
                return -1,0,0 #表示文档读完
            if self.buff[self.pointer:self.pointer+5]=='#####':
                break
            self.pointer+=1
        #content=self.buff[self.last_pointer:self.pointer]
        self.last_pointer=self.pointer+5
        self.pointer+=5
        while True:#url
            if self.pointer==self.size:
                self.read()
            if self.pointer==len(self.buff):
                return -1,0,0 #表示文档读完
            if self.buff[self.pointer:self.pointer+5]=='#####':
                break
            self.pointer+=1
        #doc_id=self.buff[self.last_pointer:self.pointer]
        self.last_pointer=self.pointer+5
        self.pointer+=5
        return doc_id,self.base_pointer+self.base_offset,self.pointer-self.base_offset

    def pop_rest(self):
        a=self.buff[self.last_pointer:]+self.filename.read(self.last_pointer)
        del self.buff
        self.buff=a
        self.pointer=self.last_pointer=self.size
        return self.buff
    def close(self):
        self.filename.close()
        del self.pointer,self.last_pointer,self.size,self.buff,self.base_pointer
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
def establish_document_index(input_file,buff_size,output_file):
    '''
    :param input_file: 网页爬取文件
    :param buff_size: 读写文件块的大小
    :param output_file: 文档号：对应此文档号的记录在文件中位置指针:此项文档占用字节数|
                                    注：起始位置为词项对应的以一个doc_id位置                                            绝对地址
                                        所占字节数 从第一个doc_id存储位置至 最后一个url存储完位置止，而不是最后的'#####'      绝对地址
    :return:
    '''
    print "process:establish document index ----->Begin"
    block_read=read_block(buff_size,input_file)
    block_write=write_block(buff_size,output_file)
    while True:
        doc_id,pointer,length=block_read.pop_token()
        if doc_id==-1:
            break
        block_write.push(doc_id+':'+str(pointer)+':'+str(length)+'|')
    block_read.close()
    block_write.close()
    del block_read
    del block_write
    print "process:establish docunment index ----->Finish"

class doc_id_index:
    dic={}
    def __init__(self,index_filename,data_filename,cache_size):
        file=open(index_filename,'r')
        self.index_file=open(data_filename,'r')
        buff=file.read()
        pointer=last_pointer=0
        if  ord(buff[0])==0xEF and  ord(buff[1])==0xBB and ord(buff[2])==0xbf : #####解决BOM问题
            pointer=last_pointer=3
        while True:
            if pointer==len(buff)-1:
                break
            #doc_id
            while True:
                if buff[pointer]==':':
                    break
                pointer+=1
            doc_id=buff[last_pointer:pointer]
            last_pointer=pointer+1
            #doc_pointer
            pointer+=1
            while True:
                if buff[pointer]==':':
                    break
                pointer+=1
            doc_pointer=buff[last_pointer:pointer]
            last_pointer=pointer+1
            #length
            pointer+=1
            while True:
                if buff[pointer]=='|':
                    break
                pointer+=1
            length=buff[last_pointer:pointer]
            last_pointer=pointer+1
            self.dic[int(doc_id)]=[int(doc_pointer),int(length)]
        file.close()
        self.cache_size=cache_size
        del buff,last_pointer,pointer,cache_size,doc_id,doc_pointer,length
        #第一次加载网页文件
        self.cache=self.index_file.read(self.cache_size)
        self.cache_pointer=0
    def get_location(self,doc_id):#pointer,doc_id_length,title_length,content_length,url_length
        if self.dic.has_key(doc_id):
            return self.dic[doc_id][0],self.dic[doc_id][1]
        else:
            print "Warning:doc_id not exist! Ignore",doc_id
            return -1,0
    def get_data(self,doc_id):
        begin_location,length=self.get_location(doc_id)
        if begin_location==-1:
            return '','','' #title content url
        if begin_location>=self.cache_pointer and begin_location+length<=self.cache_pointer+self.cache_size:
            #从内存中找
            pass
        else:
            #从磁盘中读
            if length>self.cache_size:
                print "Error:cache too small!can not load data"
                return '','',''
            else:
                del self.cache
                self.index_file.seek(begin_location,0)
                self.cache=self.index_file.read(self.cache_size)
                self.cache_pointer=begin_location
        pointer=last_pointer=begin_location-self.cache_pointer
        while True:#doc_id
            if self.cache[pointer]=='#####':
                break
            pointer+=1
        doc_id=self.cache[last_pointer:pointer]
        pointer+=5
        last_pointer=pointer
        while True:#title
            if self.cache[pointer]=='#####':
                break
            pointer+=1
        title=self.cache[last_pointer:pointer]
        pointer+=5
        last_pointer=pointer
        while True:#content
            if self.cache[pointer]=='#####':
                break
            pointer+=1
        content=self.cache[last_pointer:pointer]
        pointer+=5
        last_pointer=pointer
        while True:#url
            if self.cache[pointer]=='#####':
                break
            pointer+=1
        url=self.cache[last_pointer:pointer]
        pointer+=5
        last_pointer=pointer
        return title,content,url
    def close(self):
        del self.cache,self.cache_size,self.cache_pointer
        self.index_file.close()

establish_document_index("data/test_data.txt",20240,"data/test_index.txt")
dic=doc_id_index("data/test_index.txt","data/test_data.txt",20240)
print dic.get_data(10)
