#-*- coding: UTF-8 -*-
'''
基于相似内容的推荐：余弦相似度
'''
import Dictionary
import math
import config

path="data/netease"
class max_queue:
    '''
    用最大堆实现的优先队列
    '''
    def __init__(self,a):
        self.queue=[]
        self.queue.append([65536,'',''])
        self.queue.extend(a)
        self.queue_size=len(a)
    def output(self):
        output=self.queue[1:self.queue_size+1]
        print(output)
    def insert(self,x):#将新的元素插入
        self.queue.append(x)
        self.queue_size+=1
        self.change_key(x,self.queue_size)
    def max_quene(self,index):
        l=2*index
        r=2*index+1
        if l<=self.queue_size and self.queue[l][0]>self.queue[index][0]:
            largest=l
        else:
            largest=index
        if r<=self.queue_size and self.queue[r][0]>self.queue[largest][0]:
            largest=r
        if largest!=index:
            buff=self.queue[largest]
            self.queue[largest]=self.queue[index]
            self.queue[index]=buff
            self.max_quene(largest)
    def maximum(self):#返回最大值
        return self.queue[1]
    def extract_max(self):#O(lgn) #返回并去掉最大值
        if self.queue_size<1:
            print('Warning:extract_max ,there is no more element in quene')
            return -1,-1,-1
        else:
            buff=self.queue[1]
            self.queue[1]=self.queue[self.queue_size]
            self.queue_size-=1
            self.max_quene(1)
            return buff
    def increase_key(self,x,index):#将元素的值增加到k，其中k值不能小于此元素原先的值
        if x[0]<self.queue[index][0]:
            print('error:new key is small than current key')
        else:
            self.queue[index]=x
            parent=int(index/2)
            while parent>0 and self.queue[index][0]>self.queue[parent][0]:
                buff=self.queue[index]
                self.queue[index]=self.queue[parent]
                self.queue[parent]=buff
                index=int(index/2)
                parent=int(index/2)
    def decrease_key(self,x,index):
        if x[0]>self.queue[index][0]:
            print('error:new key is bigger than current key')
        else :
            self.queue[index]=x
            self.max_quene(index)
    def change_key(self,x,index):
        if self.queue[index][0]>x[0]:
            self.decrease_key(x,index)
        else:
            self.increase_key(x,index)
    def build_quene1(self):#利用 insert方式
        a=self.queue[1:]
        self.queue.clear()
        self.queue.append(65535)
        self.queue_size=0
        for i in range(len(a)):
            self.insert(a[i])
    def build_quene2(self):#利用  max_quene方式
        index=int(self.queue_size/2)
        while index>0:
            self.max_quene(index)
            index-=1
class min_queue:
    '''
    用最小堆实现的优先队列
    '''
    def __init__(self,a):
        self.queue=[]
        self.queue.append([-1,'',''])
        self.queue.extend(a)
        self.queue_size=len(a)
    def output(self):
        output=self.queue[1:self.queue_size+1]
        print(output)
    def insert(self,x):#将新的元素插入
        self.queue.append(x)
        self.queue_size+=1
        self.change_key(x,self.queue_size)
    def min_quene(self,index):
        l=2*index
        r=2*index+1
        if l<=self.queue_size and self.queue[l][0]<self.queue[index][0]:
            smallest=l
        else:
            smallest=index
        if r<=self.queue_size and self.queue[r][0]<self.queue[smallest][0]:
            smallest=r
        if smallest!=index:
            buff=self.queue[smallest]
            self.queue[smallest]=self.queue[index]
            self.queue[index]=buff
            self.min_quene(smallest)
    def minimum(self):#返回最大值
        return self.queue[1]
    def extract_min(self):#O(lgn) #返回并去掉最大值
        if self.queue_size<1:
            print('Warning:extract_max ,there is no more element in quene')
            return -1,-1,-1
        else:
            buff=self.queue[1]
            self.queue[1]=self.queue[self.queue_size]
            self.queue_size-=1
            self.min_quene(1)
            return buff
    def decrease_key(self,x,index):#将元素的值增加到k，其中k值不能小于此元素原先的值
        if x[0]>self.queue[index][0]:
            print('error:new key is small than current key')
        else:
            self.queue[index]=x
            parent=int(index/2)
            while parent>0 and self.queue[index][0]<self.queue[parent][0]:
                buff=self.queue[index]
                self.queue[index]=self.queue[parent]
                self.queue[parent]=buff
                index=int(index/2)
                parent=int(index/2)
    def increase_key(self,x,index):
        if x[0]>self.queue[index][0]:
            print('error:new key is bigger than current key')
        else :
            self.queue[index]=x
            self.min_quene(index)
    def change_key(self,x,index):
        if self.queue[index][0]<x[0]:
            self.increase_key(x,index)
        else:
            self.decrease_key(x,index)
    def build_quene1(self):#利用 insert方式
        a=self.queue[1:]
        self.queue.clear()
        self.queue.append(65535)
        self.queue_size=0
        for i in range(len(a)):
            self.insert(a[i])
    def build_quene2(self):#利用  max_quene方式
        index=int(self.queue_size/2)
        while index>0:
            self.min_quene(index)
            index-=1

class CosineScore:
    def __init__(self,dic_filename,inverted_index_filename,cache_size,doc_total_numbers=100000):
        self.dictionary=Dictionary.dictionary(dic_filename,inverted_index_filename,cache_size)
        self.N=doc_total_numbers
    def calculate(self,query_token_list,Top_numbers=10):
        '''
        查询词项：w=log(N/df)
        文档词项：w=(1+logtf)
        :param query_token_list:
        :return:
        '''
        doc={} #key:doc_id value:position
        scores=[] #[score,doc_id,tf]
        for i in range(len(query_token_list)):
            term=query_token_list[i]
            df,doc_id,tf=self.dictionary.get_idfANDinvertedindex(term)
            if df==0:
                pass
            else:
                w_query=math.log10(self.N/df)
                for j in range(len(doc_id)):
                    w_d=1+math.log10(tf[j])
                    if doc.has_key(doc_id[j]):
                        position=doc[doc_id[j]]
                        scores[position][0]+=w_d*w_query
                        scores[position][1]=doc_id[j]
                        scores[position][2]+=(w_d**2)
                    else:
                        position=len(scores)
                        doc[doc_id[j]]=position
                        scores.append([w_d*w_query,doc_id[j],w_d**2])
    #for k in range(len(scores)):#没有进行 归一化处理
        #scores[k][0]=scores[k][0]/(scores[k][2]**0.5)

        quene=max_queue(scores)
        quene.build_quene2()
        topK=[]
        i=0
        while True:
            id=quene.extract_max()[1]
            if id==-1 or i==Top_numbers:
                break
            i+=1
            topK.append(id)
        del doc,scores,term,df,doc_id,tf,w_query,position,quene
        return topK

class FastCosineScore:
    '''
    如何加速：
    思路一：加快每个余弦相似度的计算
    思路二：不对所有文档的评分结果排序而直接选出Top K篇文档
    思路三：能否不需要计算所有Ｎ篇文档的得分？
    :param query_token_list:
    :return:
    方法一：索引去除(Index elimination)：一般检索方法中，通常只考虑至少包含一个查询词项的文档。可以进一步拓展这种思路，
                        只考虑那些包含高idf查询词项的文档，
                        只考虑那些包含多个查询词项的文档(比如达到一定比例，3个词项至少出现2个，4个中至少出现3个等等)
    方法二：胜者表(Champion list)：对每个词项t，预先计算出其倒排记录表中权重最高的r篇文档，如果采用tfidf机制，即tf最高的r篇，这r篇文档称为t的胜者表
                                    也称为优胜表(fancy list)或高分文档(top docs)
                                    注意：r 比如在索引建立时就已经设定
                                    因此，有可能 r < K
                                    检索时，仅计算某些词项的胜者表中包含的文档集合的并集
                                    从这个集合中选出top K作为最终的top K
    '''
    def __init__(self,dic_filename,inverted_index_filename,cache_size,stopword_filename,doc_total_numbers=100000):
        self.dictionary=Dictionary.dictionary(dic_filename,inverted_index_filename,cache_size)
        self.N=doc_total_numbers

        self.stopword={}
        buff=open(stopword_filename,'r').read()
        pointer=lastpointer=0
        while pointer<len(buff):
            while buff[pointer]!='\n':
                pointer+=1
            self.stopword[buff[lastpointer:pointer]]=1
            lastpointer=pointer+1
            pointer+=1
        del buff,lastpointer,pointer

    def calculate(self,query_token_list,Top_numbers=10,multiple=10):
        '''
        查询词项：w=log(N/df)
        文档词项：w=(1+logtf)
        :param query_token_list: [word1,word2]
        :parame Top_numbers       返回的记录数
        ：param  multiple          从Top_numbers*multiple中找Top
        :return:
        '''
        doc={} #key:doc_id value:position
        scores=[] #[score,doc_id,tf]

        invert_index=[]
        for i in range(len(query_token_list)):
            df,doc_id,tf=self.dictionary.get_idfANDinvertedindex(query_token_list[i]) #
            if df==0:
                pass
            else:
                invert_index.append([df,doc_id,tf])
        quene=min_queue(invert_index)
        quene.build_quene2()#按照df排序  降序排
        while True:
            min=quene.extract_min()
            if min[0]==-1 or len(scores)>Top_numbers*multiple:
                break
            w_query=math.log10(self.N/min[0])
            for j in range(len(min[1])):
                w_d=1+math.log10(min[2][j])
                if doc.has_key(min[1][j]):
                    position=doc[min[1][j]]
                    scores[position][0]+=w_d*w_query
                    scores[position][1]=min[1][j]
                    scores[position][2]+=(w_d**2)
                else:
                    position=len(scores)
                    doc[min[1][j]]=position
                    scores.append([w_d*w_query,min[1][j],w_d**2])
        #for k in range(len(scores)):
            #scores[k][0]=scores[k][0]/(scores[k][2]**0.5)
        top=max_queue(scores)
        top.build_quene2()
        topK=[]
        while True:
            id=top.extract_max()[1]
            if id==-1 or len(topK)>Top_numbers:
                break
            topK.append(id)
        del doc,scores,w_query,position
        return topK

    def get_from_file(self,similar_filename):
        self.dic={}
        file=open(similar_filename,'r')
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
            similar_id=[]
            while True:
                #similar_doc_id
                pointer+=1
                while True:
                    if buff[pointer]==':' or buff[pointer]=='|':
                        break
                    pointer+=1
                similar_id.append(int(buff[last_pointer:pointer]))
                last_pointer = pointer + 1
                if buff[pointer]=='|':
                    break
            self.dic[int(doc_id)]=similar_id
        file.close()
