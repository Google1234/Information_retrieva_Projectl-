#-*- coding: UTF-8 -*-
import os
datapath='data/invert_index_test_'
#dicpath='data/dic_test_'
buff_path='data/buff_'


buff_size=1024*1



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
                return -1 #表示文档读完
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

'''
def sort_fie(id_list):
    if len(id_list)<=1:
        return id_list[0]
    else :
        left=id_list[:len(id_list)/2]
        right=id_list[len(id_list)/2:]
        id1=sort_fie(left)
        id2=sort_fie(right)

        file1=open(datapath+str(id1)+'.txt','r')
        file2=open(datapath+str(id2)+'.txt','r')
        output_data=open(buff_path+str(id1)+str(id2)+'.txt','w')


        output_buff=[]
        output_pointer=0






        Flag1=Flag2=False
        while Flag1==False and Flag2==False:
            if output_pointer>=buff_size:
                output_data.write(output_buff)
                output_pointer=0
                del output_buff
                output_buff=[]

            if dic_id1>dic_id2:
                while True:
                    pointer2+=1
                    if a2[pointer2]=='\n':
                        break
                output_buff.append(dic_id2)
                output_buff.append(':')
                output_buff.append(a2[last_pointer2:pointer2])
                output_buff.append('\n')
                output_pointer+=len(dic_id2)+1+(pointer2-last_pointer2)+1
                last_pointer2=pointer2+1



            if dic_id2>dic_id1:
                while True:
                    pointer1+=1
                    if a1[pointer1]=='\n':
                        break
                output_buff.append(dic_id1)
                output_buff.append(':')
                output_buff.append(a1[last_pointer1:pointer1])
                output_buff.append('\n')
                output_pointer+=len(dic_id1)+1+(pointer1-last_pointer1)+1
                last_pointer1=pointer1+1

                while True:
                    pointer1+=1
                    if a1[pointer1]=='':
                        Flag1=True
                        break
                    if a1[pointer1]==':':
                        break
                dic_id1=a1[last_pointer1:pointer1]
            if dic_id1==dic_id2:
                output_buff.append(dic_id1)
                output_buff.append(':')
                output_pointer+=(pointer1-last_pointer1)+1
                last_pointer1=pointer1+1
                last_pointer2=pointer2+1

                while True:
                    pointer1+=1
                    if a1[pointer1]=='#':
                        break
                doc_id1=a1[last_pointer1:pointer1]

                while True:
                    pointer2+=1
                    if a2[pointer2]=='#':
                        break
                doc_id2=a2[last_pointer2:pointer2]

                Stop1=Stop2=False
                while Stop1==False and Stop2==False:
                    if doc_id1>doc_id2:
                        last_pointer2=pointer2+1
                        while True:
                            pointer2+=1
                            if a2[pointer2]=='\n':
                                Stop2=True
                            if a2[pointer2]==':':
                                break
                        output_buff.append(doc_id2)
                        output_buff.append('#')
                        output_buff.append(a2[last_pointer2:pointer2])
                        output_buff.append(':')
                        output_pointer+=len(doc_id2)+1+(pointer2-last_pointer2)+1
                        last_pointer2=pointer2+1

                        while True:
                            pointer2+=1
                            if a2[pointer2]=='#':
                                break
                        doc_id2=a2[last_pointer2:pointer2]

                    if doc_id2>doc_id1:
                        last_pointer1=pointer1+1
                        while True:
                            pointer1+=1
                            if a1[pointer1]=='\n':
                                Stop1=True
                                break
                            if a1[pointer1]==':':
                                break
                        output_buff.append(doc_id1)
                        output_buff.append('#')
                        output_buff.append(a1[last_pointer1:pointer1])
                        output_buff.append(':')
                        output_pointer+=len(doc_id1)+1+(pointer1-last_pointer1)+1
                        last_pointer1=pointer1+1

                        while True:
                            pointer1+=1
                            if a1[pointer1]=='#':
                                break
                        doc_id1=a1[last_pointer1:pointer1]

                    if doc_id2==doc_id1:
                        output_buff.append(doc_id1)
                        output_buff.append('#')
                        output_pointer+=(pointer1-last_pointer1)+1
                        last_pointer1=pointer1+1
                        last_pointer2=pointer2+1


                        while True:
                            pointer1+=1
                            if a1[pointer1]=='\n':
                                Stop1=True
                                break
                            if a1[pointer1]==':':
                                break
                        #numbers1=a1[last_pointer1:pointer1]
                        while True:
                            pointer2+=1
                            if a2[pointer2]=='\n':
                                Stop2=True
                                break
                            if a2[pointer2]==':':
                                break
                        #numbers2=a2[last_pointer2:pointer2]

                        #output_buff.append(str(int(numbers1)+int(numbers2)))
                        output_buff.append(str(int(a1[last_pointer1:pointer1])+int(a2[last_pointer2:pointer2])))
                        output_buff.append(':')
                        output_pointer+=(pointer1-last_pointer1)+(pointer2-last_pointer2)+1
                        last_pointer1=pointer1+1
                        last_pointer2=pointer2+1

                        while True:
                            pointer1+=1
                            if a1[pointer1]=='#':
                                break
                        doc_id1=a1[last_pointer1:pointer1]
                        while True:
                            pointer2+=1
                            if a2[pointer2]=='#':
                                break
                        doc_id2=a2[last_pointer2:pointer2]
                if Stop1==True:
                    while True:
                        pointer2+=1
                        if a2[pointer2]=='\n':
                            break
                    output_buff.append(a2[last_pointer2:pointer2])
                    output_buff.append('\n')
                    output_pointer+=(pointer2-last_pointer2)
                    last_pointer2=pointer2+1
                if Stop2==True:
                    while True:
                        pointer1+=1
                        if a1[pointer1]=='\n':
                            break
                    output_buff.append(a1[last_pointer1:pointer1])
                    output_buff.append('\n')
                    output_pointer+=(pointer1-last_pointer1)
                    last_pointer1=pointer1+1

                while True:
                    pointer1+=1
                    if a1[pointer1]=='':
                        Flag1=True
                        break
                    if a1[pointer1]==':':
                        break
                dic_id1=a1[last_pointer1:pointer1]
                while True:
                    pointer2+=1
                    if a2[pointer2]=='':
                        Flag2=True
                        break
                    if a2[pointer2]==':':
                        break
                dic_id2=a2[last_pointer2:pointer2]

        if Flag1==True:
            pointer2=buff_size
            while True:
                pointer2-=1
                if a2[pointer2]=='\n':
                    output_buff.append(a2[last_pointer2:pointer2+1])
                    last_buff1=a2[]
                    break
            output_buff.append(a2[last_pointer2:pointer2])
            output_pointer+=(pointer2-last_pointer2)
            last_pointer2=pointer2+1
        if Flag2==True:
            while True:
                pointer1+=1
                if a1[pointer1]=='':
                    break
            output_buff.append(a1[last_pointer1:pointer1])
            output_pointer+=(pointer1-last_pointer1)
            last_pointer1=pointer1+1




        buff=open(buff_path+str(id1)+str(id2)+'.txt','w')
        line1=file1.readline()[:-1]  #要求文档结尾必须有'\n',否则会乱码
        line2=file2.readline()[:-1]  #要求文档结尾必须有'\n',否则会乱码
        while line1!='' and line2!='':
            if line1<line2:
                buff.writelines(line1+'\n')
                line1=file1.readline()[:-1]
            else:
                if line1==line2:
                    buff.writelines(line2+'\n')
                    line1=file1.readline()[:-1]
                    line2=file2.readline()[:-1]
                else:
                    buff.writelines(line2+'\n')
                    line2=file2.readline()[:-1]
        if line1=='':
            block=file2.read(max_size)
            buff.write(line2+'\n')
            while block!='':
                buff.write(block)
                del block
                block=file2.read(max_size)
        else:
            block=file1.read(max_size)
            buff.write(line1+'\n')
            while block!='':
                buff.write(block)
                del block
                block=file1.read(max_size)
        file1.close()
        file2.close()
        buff.close()

#sort_fie([1,2])

'''

