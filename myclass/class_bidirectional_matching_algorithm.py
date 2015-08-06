# -*- coding: utf-8 -*-
# !/usr/bin/python
################################### PART0 DESCRIPTION #################################
# Filename: class_bidirectional_matching_algorithm.py
# Description: Accomplish bidirectional matching algorithm
#           (which is based on RMM and MM methods) in Chinese word segmentation.
#           Therefore, in class_bidirectional_matching_algorithm.py file,
#           I realized 3 methods in Chinese word segmentation,
#           and made comparison and evaluation of these 3 methods.

# Author: Shuai Yuan
# E-mail: ysh329@sina.com
# Create: 2015-7-31 15:54:22
# Last:
__author__ = 'yuens'
################################### PART1 IMPORT ######################################
import MySQLdb
import sys
import re
import time
################################### PART2 CLASS && FUNCTION ###########################
class ChineseWordSegmentation(object):
    def __init__(self):
        self.start = time.clock()

    def __del__(self):
        self.end = time.clock()
        print "elapsed time:%0.3f" % (self.end - self.start)

    def pre_process(self, raw_string, sign_list):

        split_index_list = map(lambda sign: raw_string.find(sign), sign_list)
        split_index_list = filter(lambda index: index > - 1, split_index_list)
        split_index_list = sorted(split_index_list, reverse=True)

        print "raw_string:", raw_string
        print "raw_string.split('='):", raw_string.split("=")
        print "split_index_list:", split_index_list

        cur_raw_string = raw_string
        sentence_list = []
        for idx in xrange(len(split_index_list)):
            split_index = split_index_list[idx]
            if split_index+1 == len(cur_raw_string):
                continue
                #cur_raw_string = cur_raw_string[:split_index]
            sentence_list.append(cur_raw_string[split_index+1:])
        print sentence_list
        sentence_list.append(cur_raw_string[:split_index])
        # cur_raw_string namely is ""
        print "sentence_list:", sentence_list

    def find_index(self, raw_string, sign):
        cur_string = raw_string
        index_list = []
        index = cur_string.rfind(sign)
        while index:
            index_list.append(index)
            cur_string = cur_string[:index]
            index = cur_string.rfind(sign)
            if cur_string == sign: index_list.append(index)
        return index_list




    def remove_stopwords(self, sentence):
        pass

    def maximum_matching(self, sentence):
        pass

    def reverse_maximun_matching(self, sentence):
        pass

    def bidirectional_maximum_matching(self, sentence):
        pass
################################### PART3 CLASS TEST ##################################
# initial parameters
sign_list = ["。", "，", "！", "？", "?", "`", "~",\
						 "!", "@", "#", "$", "%", "^", "&",\
						 "*", "(", ")", "_", "+", "—", "=",\
						 "＝", "-", "_", "）","（", "…", "￥",\
						 "！", "；", ";", "：", ":", "‘", "”",\
						 "“", ", ", "{", "}", "|", "、", "】", "【",\
						 ".", "\\", "/", "<", ">", "《", "》",\
						 " ", "·", "    ", " ", "―", "［", "］"]
'''
raw_string = "123=45-67+"
raw_string = "+++123+45+67+++"
raw_string = "+"
raw_string = "+++"
'''

test = ChineseWordSegmentation()
#test.pre_process(raw_string = raw_string, sign_list = sign_list)
print test.find_index(raw_string, "+")
