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
            print "idx:", idx

            split_index = split_index_list[idx]
            print "split_index:", split_index
            if split_index + 1 == len(raw_string):
                cur_raw_string = cur_raw_string[:split_index]
            elif idx + 1 == len(split_index_list):
                sentence = cur_raw_string[:split_index]
                sentence_list.append(sentence)
                break
            else:
                split_start_index = split_index + 1
                sentence = cur_raw_string[split_start_index:]
                sentence_list.append(sentence)
                cur_raw_string = cur_raw_string[:split_index]


            print "cur_raw_string:", cur_raw_string
        print "sentence_list:", sentence_list








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
raw_string = "123=45-67+"

test = ChineseWordSegmentation()
test.pre_process(raw_string = raw_string, sign_list = sign_list)
