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

    def pre_process(self, raw_string):
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
raw_string = ""
test = ChineseWordSegmentation()