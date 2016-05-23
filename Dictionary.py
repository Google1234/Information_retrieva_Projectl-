#-*- coding: UTF-8 -*-
class read_block:
    def __init__(self,buff_size,filename):
        self.size=buff_size
        self.filename=open(filename,'r')
        self.buff=self.filename.read(self.size)
        self.pointer=0
        if  ord(self.buff[0])==0xEF and  ord(self.buff[1])==0xBB and ord(self.buff[2])==0xbf : #####解决BOM问题
            self.last_pointer=3
            self.token_pointer=3
        else:
            self.last_pointer=0
            self.token_pointer=0
        self.base_pointer=0
    def read(self):
        if self.last_pointer==0:
            print "Error! :self.size is too small !self.buff is full,can not load new data!"
        a=self.buff[self.last_pointer:]+self.filename.read(self.last_pointer)
        del self.buff
        self.buff=a
        self.pointer-=self.last_pointer
        self.base_pointer+=self.last_pointer
        self.token_pointer-=self.last_pointer
        self.last_pointer=0
    def pop_token(self):
        '''
        返回 词项倒排记录相关值
        :return: word   词项
                  idf    词项idf  数值型
                  offset 词项对应的第一个doc_id 存储的位置与上一个词项              数值型
                  length         词项doc_id tf 所占的字节数,不包括末尾的'|'    数值型
        '''
        while True:#word
            if self.pointer==self.size:
                self.read()
            if self.pointer==len(self.buff):
                return '','',0,0 #表示文档读完
            if self.buff[self.pointer]==':':
                break
            self.pointer+=1
        word=self.buff[self.last_pointer:self.pointer]
        self.last_pointer=self.pointer+1
        self.token_pointer=self.pointer+1
        #doc_id=[]
        #tf=[]
        idf=0
        while True:
            while True:#page
                if self.pointer==self.size:
                    self.read()
                if self.buff[self.pointer]=='#':
                    break
                self.pointer+=1
            #doc_id.append(self.buff[self.last_pointer:self.pointer])
            idf+=1
            self.last_pointer=self.pointer+1
            while True:#tf
                if self.pointer==self.size:
                    self.read()
                if self.buff[self.pointer]=='|':
                    #tf.append(self.buff[self.last_pointer:self.pointer])
                    self.last_pointer=self.pointer+1
                    return word,idf,self.token_pointer+self.base_pointer,self.pointer-self.token_pointer
                if self.buff[self.pointer]==':':
                    break
                self.pointer+=1
            #tf.append(self.buff[self.last_pointer:self.pointer])
            self.last_pointer=self.pointer+1

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
def establish_ditionary(input_file,buff_size,output_file):
    '''
    :param input_file: 倒排索引文件
    :param buff_size: 读写文件块的大小
    :param output_file: 词项：idf：词项在倒排记录表中位置指针:词项倒排索引所占的字节数|
                                    注：起始位置为词项对应的以一个doc_id位置                                            绝对地址
                                        所占字节数 从第一个doc_id存储位置至 最后一个tf存储位置止，而不是最后的'|'      绝对地址
    :return:
    '''
    print "process:establish index dictionnary----->Begin"
    block_read=read_block(buff_size,input_file)
    block_write=write_block(buff_size,output_file)
    while True:
        word,idf,begin_pointer,offset=block_read.pop_token()
        if word=='':
            break
        block_write.push(word+':'+str(idf)+':'+str(begin_pointer)+':'+str(offset)+'|')
    block_read.close()
    block_write.close()
    del block_read
    del block_write
    print "process:establish index dictionnary----->Finish"
class dictionary:
    dic={}
    def __init__(self,Dic_filename,inverted_index_filename,cache_size):
        '''
        从文件中加载字典
        :param 字典文件名:
        :return: NOne
        '''
        file=open(Dic_filename,'r')
        self.index_file=open(inverted_index_filename,'r')
        buff=file.read()
        pointer=last_pointer=0
        if  ord(buff[0])==0xEF and  ord(buff[1])==0xBB and ord(buff[2])==0xbf : #####解决BOM问题
            pointer=last_pointer=3
        while True:
            if pointer==len(buff)-1:
                break
            #word
            while True:
                if buff[pointer]==':':
                    break
                pointer+=1
            word=buff[last_pointer:pointer]
            last_pointer=pointer+1
            #idf
            pointer+=1
            while True:
                if buff[pointer]==':':
                    break
                pointer+=1
            idf=buff[last_pointer:pointer]
            last_pointer=pointer+1
            #begin_pointer
            pointer+=1
            while True:
                if buff[pointer]==':':
                    break
                pointer+=1
            begin_pointer=buff[last_pointer:pointer]
            last_pointer=pointer+1
            #offset_pointer
            pointer+=1
            while True:
                if buff[pointer]=='|':
                    break
                pointer+=1
            offset=buff[last_pointer:pointer]
            last_pointer=pointer+1
            self.dic[word]=[int(idf),int(begin_pointer),int(offset)]
            del word,idf,begin_pointer,offset
        file.close()
        self.cache_size=cache_size
        del buff,last_pointer,pointer,cache_size
        #第一次加载倒排记录表
        self.cache=self.index_file.read(self.cache_size)
        self.cache_pointer=0
    def get_idfANDlocation(self,word):#idf,begin_location,length
        if self.dic.has_key(word):
            return self.dic[word][0],self.dic[word][1],self.dic[word][2]
        else:
            print "Warning:word not exist! Ignore",word
            return 0,0,0
    def get_idfANDinvertedindex(self,word):
        '''
        从倒排记录表中返回词项的倒排记录
        :param word: 词项
        :return: idf 词项倒排记录   ;倒排记录表包括doc_id 和df ====>>输出已经转换成 整形
        '''
        idf,begin_location,offset=self.get_idfANDlocation(word)
        if idf==0:
            return 0,[0],[0]
        if begin_location>=self.cache_pointer and begin_location+offset<=self.cache_pointer+self.cache_size:
            #从内存中找
            pass
        else:
            #从磁盘中读
            if offset>self.cache_size:
                print "Error:cache too small!can not load data"
                return 0
            else:
                del self.cache
                self.index_file.seek(begin_location,0)
                self.cache=self.index_file.read(self.cache_size)
                self.cache_pointer=begin_location
        pointer=last_pointer=begin_location-self.cache_pointer

        doc_id=[]
        tf=[]
        Flag=True
        while Flag:
            while True:#doc_id
                if self.cache[pointer]=='#':
                    break
                pointer+=1
            doc_id.append(self.cache[last_pointer:pointer])
            last_pointer=pointer+1
            while True:#tf
                if self.cache[pointer]=='|':
                    Flag=False
                    break
                if self.cache[pointer]==':':
                    break
                pointer+=1
            tf.append(self.cache[last_pointer:pointer])
            last_pointer=pointer+1
        del begin_location,offset,pointer,last_pointer,Flag
        return idf,[int(doc_id[i]) for i in range(len(doc_id))],[int(tf[j]) for j in range(len(tf))]
    def close(self):
        del self.cache,self.cache_size,self.cache_pointer
        self.index_file.close()