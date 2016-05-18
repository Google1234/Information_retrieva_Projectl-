#-*- coding: UTF-8 -*-
import jieba
import merge_inverted_files
def merger_sort(seq):
    if len(seq)<=1:
        return seq
    mid=int(len(seq)/2)
    left=merger_sort(seq[:mid])
    right=merger_sort(seq[mid:])
    return merger(left,right)
def merger(list1,list2):
    array=[]
    list1_len=len(list1)
    list2_len=len(list2)
    index1=0
    index2=0

    while index1<list1_len and index2<list2_len:
        if list1[index1]<=list2[index2]:
            array.append(list1[index1])
            index1+=1
        else:
            array.append(list2[index2])
            index2+=1

    while index1<list1_len:
        array.append(list1[index1])
        index1+=1
    while index2<list2_len:
        array.append(list2[index2])
        index2+=1
    return array
class read_block:
    '''
    doc_id#####title#####content#####url#####
    '''
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
        while True:#doc_id
            if self.pointer==self.size:
                self.read()
            if self.pointer==len(self.buff):
                return '','' #表示文档读完
            if self.buff[self.pointer:self.pointer+5]=='#####':
                break
            self.pointer+=1
        doc_id=self.buff[self.last_pointer:self.pointer]
        self.pointer+=4
        self.last_pointer=self.pointer+1
        while True:#title
            if self.pointer==self.size:
                self.read()
            if self.buff[self.pointer:self.pointer+5]=='#####':
                break
            self.pointer+=1
        #title=(self.buff[self.last_pointer:self.pointer])
        self.pointer+=4
        self.last_pointer=self.pointer+1
        while True:#content
            if self.pointer==self.size:
                self.read()
            if self.buff[self.pointer:self.pointer+5]=='#####':
                break
            self.pointer+=1
        content=(self.buff[self.last_pointer:self.pointer])
        self.pointer+=4
        self.last_pointer=self.pointer+1

        while True:#url
            if self.pointer==self.size:
                self.read()
            if self.buff[self.pointer:self.pointer+6]=='#####'+'\n':
                break
            self.pointer+=1
        #title=(self.buff[self.last_pointer:self.pointer])
        self.pointer+=5
        self.last_pointer=self.pointer+1
        return doc_id,content

    def close(self):
        self.filename.close()
        del self.pointer,self.last_pointer,self.size,self.buff
class SPIMI_Invert:
    '''
    SPIMI-Invert(Token_stream)
    output.file=NEWFILE()
    dictionary = NEWHASH()
    while (free memory available)
        do token <-next(token_stream) //逐一处理每个词项-文档ID对
            if term(token) !(- dictionary
               /*如果词项是第一次出现，那么加入hash词典，同时，建立一个新的倒排索引表*/
               then postings_list = AddToDictionary(dictionary,term(token))
            /*如果不是第一次出现，那么直接返回其倒排记录表，在下面添加其后*/
            else postings_list = GetPostingList(dictionary,term(token))
        if full(postings_list)
            then postings_list =DoublePostingList(dictionary,term(token))
        /*SPIMI与BSBI的区别就在于此，前者直接在倒排记录表中增加此项新纪录*/
        AddToPosTingsList (postings_list,docID(token))
    sorted_terms <- SortTerms(dictionary)
    WriteBlockToDisk(sorted_terms,dictionary,output_file)
    return output_file
    '''
    def __init__(self,filename):
        self.filename=filename
        self.dic={}
        self.block=[]
    def push_id(self,id):
        self.doc_id=id
    def push_word(self,token):
        if token=='':
            sort=merger_sort(self.dic.keys())
            invert_index_file=open(self.filename,'w')
            for i in range(len(sort)):
                index=self.dic[sort[i]]
                invert_index_file.write(sort[i].encode('utf-8'))
                j1=j2=0
                while j2<len(self.block[index]):
                    while j2<len(self.block[index]) and self.block[index][j1]==self.block[index][j2]:
                        j2+=1
                    invert_index_file.write(':'+self.block[index][j1]+'#'+str(j2-j1))
                    j1=j2
                invert_index_file.write('\n')
                '''
              写入tex数据格式：词项：文档号#次数:文档号#次数\n
              '''
            del self.block
            del self.dic
            del sort
            invert_index_file.close()
        else:
            if self.dic.has_key(token)==False:
                self.dic[token]=len(self.block)
                self.block.append([])
            self.block[self.dic[token]].append(self.doc_id)
def inverted_index(filename,read_buff_size,output_file_record_size):
    '''
    :param filename: 网页数据，包含后缀.txt
    :param read_buff_size:按块读文件，每个块的大小
    :param output_file_token_size:输出每个文件中包含的新闻纪录数
    :return:倒排索引文件
    '''
    '''
    读文件，分词，存储倒排索引至多个文件
    '''
    block_read=read_block(read_buff_size,filename)
    punct = set(u''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
    ﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
    々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
    ︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')
    file_numbers=1
    while True:
        spimi=SPIMI_Invert(filename[:-4]+str(file_numbers)+'.txt')
        count=0
        while True:
            doc_id,content=block_read.pop_token()
            if content==''or count==output_file_record_size:
                break
            content_list=jieba.lcut_for_search(content)
            spimi.push_id(doc_id)
            for j in range(len(content_list)):
                if  content_list[j] not in punct:
                    spimi.push_word(content_list[j])
            del content_list,doc_id,content
            count+=1
        spimi.push_word('')#为空 表示写文件
        if content=='':
            break
        file_numbers+=1
    '''
    合并倒排索引文件
    '''
    merge_inverted_files.merge_fie([i for i in range(1,file_numbers)],buff_size,filename[:-4])
    '''
    由倒排索引文件构建 词-倒排索引位置
    '''


buff_size=1024*1024*1
#inverted_index("data/netease_data.txt",buff_size,5000)
datapath='data/netease_data'
merge_inverted_files.merge_file([str(i) for i in range(1,8)],buff_size,datapath)