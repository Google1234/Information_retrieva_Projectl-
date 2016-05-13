#-*- coding: UTF-8 -*-
import jieba

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
class SPIMI_Invert:
    def __init__(self,filename):
        self.filename=filename
        self.dic={}
        self.block=[]
    def push_id(self,id):
        self.doc_id=id
    def push_word(self,token):
        if token=='':
            sort=merger_sort(self.dic.keys())
            dic_file=open('dic_'+self.filename+'.txt','w')
            invert_index_file=open('invert_index_'+self.filename+'.txt','w')
            for i in range(len(sort)):
                dic_file.write(sort[i].encode('utf-8'))
                dic_file.write('\n')
                index=self.dic[sort[i]]
                for j in range(len(self.block[index])):
                    invert_index_file.write(self.block[index][j])
            del self.block
            del self.dic
            del sort
            dic_file.close()
            invert_index_file.close()
        else:
            if self.dic.has_key(token)==False:
                self.dic[token]=len(self.block)
                self.block.append([])
            self.block[self.dic[token]].append(self.doc_id)



f=open("tutorial/test.txt",'r')
buff_size=1024*100
page_part_pointer=0
last_buff=''
punct = set(u' 'u''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')
buff_times=0
while True:
   a=f.read(buff_size)
   buff_times+=1
   spimi=SPIMI_Invert("netease_"+str(buff_times))
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
                        #print page_id
                    if page_part_pointer%4==2:#保存 当前网页内容
                        page_content=a[last_i:i]
                        content_list=jieba.lcut_for_search(page_content)
                        #print content_list
                        spimi.push_id(page_id)
                        for j in range(len(content_list)):
                            if content_list[j] not in punct  :
                                #print page_id,content_list[j]
                                spimi.push_word(content_list[j])
                        del content_list
                    i+=5
                    last_i=i
                    page_part_pointer+=1
            else:
                i+=1
        last_buff=a[last_i:i]
        del a
   spimi.push_word('')


