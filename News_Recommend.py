#-*- coding: UTF-8 -*-
'''
基于相似内容的推荐：余弦相似度
'''

import Dictionary
import math
class queue:
    '''
    用最大堆实现的优先队列
    '''
    queue=[]
    queue_size=0
    def __init__(self,a):
        self.queue.append([65536,''])
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
            print('error:extract_max ,there is no element in quene')
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
def CosineScore(query_token_list,Topk_numbers=10):
    '''
    查询词项：w=log(N/df)
    文档词项：w=(1+logtf)
    :param query_token_list:
    :return:
    '''
    dictionary=Dictionary.dictionary("data/netease_dataDictionary.txt","data/netease_data_inverted_index.txt",1024*1024*10)
    doc={} #key:doc_id value:position
    scores=[] #[score,doc_id,tf]
    for i in range(len(query_token_list)):
        term=query_token_list[i]
        df,doc_id,tf=dictionary.get_idfANDinvertedindex(term)
        w_query=math.log10(df)
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
    for k in range(len(scores)):
        scores[k][0]=scores[k][0]/(scores[k][2]**0.5)

    max_quene=queue(scores)
    max_quene.build_quene2()
    topK=[]
    i=0
    while True:
        id=max_quene.extract_max()[1]
        if id==-1 or i==Topk_numbers:
            break
        i+=1
        topK.append(id)
    return topK

def FastCosineScore(query_token_list):
    '''
    如何加速：
    思路一：加快每个余弦相似度的计算
    思路二：不对所有文档的评分结果排序而直接选出Top K篇文档
    思路三：能否不需要计算所有Ｎ篇文档的得分？
    :param query_token_list:
    :return:
    '''
    return



print CosineScore(["杨丹"])