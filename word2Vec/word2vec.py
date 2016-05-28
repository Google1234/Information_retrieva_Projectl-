#-*- coding: UTF-8 -*-
#gcc -c -fPIC distance.c
#gcc -shared distance.o -o distance.so
from ctypes import *
import os
class WORD(Structure):
    _fields_ = [("char", c_char_p)]
class RESULT(Structure):
    _fields_ = [("word", WORD*40),
                ("distance",c_float*40),
                ("length",c_int)]

class WORD2VEC:
    def __init__(self,so_filename,bin_filename):
        self.word2vec_distance = cdll.LoadLibrary(so_filename+'word2Vec/distance.so')
        self.word2vec_distance.loadFile(bin_filename)
        self.word2vec_distance.cal.restype = RESULT
    def cal(self,word):
        self.result= self.word2vec_distance.cal(word)

