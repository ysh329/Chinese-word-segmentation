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
        print "start pre process at " + time.strftime('%Y-%m-%d %X', time.localtime())
        reversed_split_index_list = map(lambda sign: self.find_index(raw_string = raw_string, sign = sign), sign_list)
        reversed_split_index_list = list( sorted(set(sum(reversed_split_index_list, [])), reverse=True) )
        print "reversed_split_index_list:", reversed_split_index_list
        sentence_list = self.split_raw_string_into_sentence_list(raw_string = raw_string, reversed_split_index_list = reversed_split_index_list)
        print "sentence_list:", sentence_list

        print "end pre process at " + time.strftime('%Y-%m-%d %X', time.localtime())

    def find_index(self, raw_string, sign):
        cur_string = raw_string
        index_list = []
        for idx in xrange(raw_string.count(sign)):
            index = cur_string.rfind(sign)
            index_list.append(index)
            cur_string = cur_string[:index]
        return index_list


    def split_raw_string_into_sentence_list(self, raw_string, reversed_split_index_list):
        cur_string = raw_string
        sentence_list = []
        # split list is []
        if reversed_split_index_list == []: sentence_list.append(cur_string)
        for idx in xrange(len(reversed_split_index_list)):
            split_index = reversed_split_index_list[idx]
            # last element is sign
            if split_index == len(cur_string) - 1:
                cur_string = cur_string[:split_index]
                continue
            # first segment appendix to sentence_list
            if reversed_split_index_list.index(split_index) == len(reversed_split_index_list) - 1 and len(cur_string) > 1:
                sentence_list.append(cur_string[:split_index])
            # normal split
            sentence_list.append(cur_string[split_index+1:])
            cur_string = cur_string[:split_index]
        #print "cur_string:", cur_string
        return sentence_list

    def get_sentence_stopwords_list(self, database_name, table_name):
        pass


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
'''
sign_list = ["。", "，", "！", "？", "?", "`", "~",\
						 "!", "@", "#", "$", "%", "^", "&",\
						 "*", "(", ")", "_", "+", "—", "=",\
						 "＝", "-", "_", "）","（", "…", "￥",\
						 "！", "；", ";", "：", ":", "‘", "”",\
						 "“", ", ", "{", "}", "|", "、", "】", "【",\
						 ".", "\\", "/", "<", ">", "《", "》",\
						 " ", "·", "    ", " ", "―", "［", "］"]
'''
sign_list = [".", "?", "!", "。", "，", "？", "！", "+"]



'''
raw_string = "123=45-67+"

raw_string = "+"
raw_string = "+++"
'''
raw_string = "1234567"
print "raw_string:", raw_string
test = ChineseWordSegmentation()
print test.pre_process(raw_string = raw_string, sign_list = sign_list)
#print test.find_index(raw_string = raw_string, sign = "+")