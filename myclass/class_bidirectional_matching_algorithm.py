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
import gc
################################### PART2 CLASS && FUNCTION ###########################
class ChineseWordSegmentation(object):
    def __init__(self, database_name):
        print "start at:" + time.strftime('%Y-%m-%d %X', time.localtime())
        self.start = time.clock()
        try:
            self.con = MySQLdb.connect(host = "localhost", user = "root", passwd = "931209", db = database_name, charset = "utf8")
            print "connected MySQL successfully."
        except MySQLdb.Error, e:
            print 'failed in connecting database %s.' % database_name
            print 'MySQL Error %d: %s.' % (e.args[0], e.args[1])



    def __del__(self):
        self.end = time.clock()
        self.con.close()
        print "elapsed time:%0.3f" % (self.end - self.start)
        print "end at:" + time.strftime('%Y-%m-%d %X', time.localtime())



    def split_raw_string_into_sentence_process(self, raw_string, sign_list):
        #print "start pre process at " + time.strftime('%Y-%m-%d %X', time.localtime())
        reversed_split_index_list = map(lambda sign: self.find_index(raw_string = raw_string, sign = sign), sign_list)
        reversed_split_index_list = list( sorted(set(sum(reversed_split_index_list, [])), reverse=True) )
        #print "reversed_split_index_list:", reversed_split_index_list

        sentence_list = self.split_raw_string_into_sentence_list(raw_string = raw_string, reversed_split_index_list = reversed_split_index_list)
        #for sentence in sentence_list: print sentence

        #print "end pre process at " + time.strftime('%Y-%m-%d %X', time.localtime())
        return sentence_list


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



    def get_essay_list(self, database_name, table_name):
        """get title and content of essays from one table of database 'essayDB'."""
        essay_list = []
        cursor = self.con.cursor()
        try:
            sql = """SELECT id, title, content FROM %s.%s WHERE id<5""" % (database_name, table_name)
            cursor.execute(sql)
            essay_tuple = cursor.fetchall()
            """
            print "len(essay_tuple):", len(essay_tuple)
            print "type(essay_tuple):", type(essay_tuple)
            print
            print "essay_tuple[0]:", essay_tuple[0]
            print "len(essay_tuple[0]):", len(essay_tuple[0])
            print "type(essay_tuple[0]):", type(essay_tuple[0])
            print
            print "essay_tuple[0][0]:", essay_tuple[0][0]
            print "essay_tuple[0][1]:", essay_tuple[0][1]
            print "essay_tuple[0][2]:", essay_tuple[0][2]
            print "type(essay_tuple[0][1]):", type(essay_tuple[0][1])
            """
            if len(essay_tuple) > 1:
                for idx in xrange(len(essay_tuple)):
                    id = int(essay_tuple[idx][0])
                    title = essay_tuple[idx][1]
                    content = essay_tuple[idx][2]
                    try:
                        if type(title) != unicode: title = unicode(title, "utf8")
                        if type(content) != unicode: content = unicode(content, "utf8")
                        essay_list.append([id, title, content])
                    except:
                        print "transform encoding to unicode failed."
                        print "essay_tuple[0][0]:", essay_tuple[0][0]
                        print "essay_tuple[0][1]:", essay_tuple[0][1]
                        print "essay_tuple[0][2]:", essay_tuple[0][2]
                        continue
        except MySQLdb.Error, e:
            print "failed in selecting stopwords from table %s database %s." % (table_name, database_name)
            print "MySQL Error %d: %s." % (e.args[0], e.args[1])

        print "Get essay list successfully."
        print "Get essay record %s." % (len(essay_list))
        return essay_list



    def get_word_list(self, database_name, table_name):
        word_list = []

        cursor = self.con.cursor()
        try:
            sql = """SELECT word FROM %s.%s WHERE type1='t1'""" % (database_name, table_name)
            #sql = """SELECT word FROM %s.%s""" % (database_name, table_name)
            cursor.execute(sql)
            word_tuple = cursor.fetchall()
            if len(word_tuple) > 0:
                for idx in xrange(len(word_tuple)):
                    try:
                        word = word_tuple[idx][0]
                        if type(word) != unicode: word = unicode(word, "utf8")
                        word_list.append(word)
                    except:
                        print "failed in transforming word %s to unicode form." % word
                        print "word %s %s" % (word, type(word))
                        continue
            print "get words %s from database successfully." % len(word_list)
        except MySQLdb.Error, e:
            print 'failed in selecting words from database %s.' % database_name
            print 'MySQL Error %d: %s.' % (e.args[0], e.args[1])
        return word_list



    def get_sentence_stopword_list(self, database_name, table_name):
        stopword_list = [] # unicode stopword

        cursor = self.con.cursor()
        try:
            sql = """SELECT word FROM %s.%s WHERE type1='stopword'""" % (database_name, table_name)
            cursor.execute(sql)
            stopword_tuple = cursor.fetchall()
            '''
            print "stopword_tuple:", stopword_tuple
            print "len(stopword_tuple):", len(stopword_tuple)
            print "type(stopword_tuple):", type(stopword_tuple)
            print "stopword_tuple[0]:", stopword_tuple[0]
            print "stopword_tuple[0][0]:", stopword_tuple[0][0]
            print "type(stopword_tuple[0][0]):", type(stopword_tuple[0][0])
            '''
            if len(stopword_tuple) > 0:
                for idx in xrange(len(stopword_tuple)):
                    try:
                        stopword = stopword_tuple[idx][0]
                        if type(stopword) != unicode: stopword = unicode(stopword, "utf8")
                        stopword_list.append(stopword)
                    except:
                        print "failed in transforming stopword %s to unicode form." % stopword_tuple[idx][0]
                        print "stopword %s %s" % (stopword, type(stopword))
                        continue
            print "get stopwords %s from database successfully." % len(stopword_list)
        except MySQLdb.Error, e:
            print 'failed in selecting stopwords from database %s.' % database_name
            print 'MySQL Error %d: %s.' % (e.args[0], e.args[1])
        return stopword_list



    def get_string_or_list_unicode(self, string_or_list):

        if type(string_or_list) == None:
            return ""
        if type(string_or_list) == list:
            unicode_list = []
            for i in range(len(string_or_list)):
                if type(string_or_list[i]) == unicode:
                    unicode_list.append(string_or_list[i])
                    if i == len(string_or_list) - 1:
                        unicode_list = string_or_list
                        return unicode_list
                    continue
                else: # type(string_or_list[i] != unicode)
                    try:
                        unicode_list.append(unicode(string_or_list[i], "utf8"))
                    except:
                        print "[get_sth_unicode]The element of list's type is not UFT8."
                        print "[get_sth_unicode]OR the original list's type is UNICODE."
                        print "[get_sth_unicode]What it is:", string_or_list[i]
                        print "[get_sth_unicode]What it's type:", type(string_or_list[i])
                        print "[get_sth_unicode]Ignore this element in list(continue execute)."
                        continue
            return unicode_list
        elif type(string_or_list) == str:
            try:
                unicode_string = unicode(string_or_list, "utf8")
                return unicode_string
            except:
                print "[get_sth_unicode]The string's type is not utf8."
                print "[get_sth_unicode]OR the string's type is UNICODE."
                print "[get_sth_unicode]Return original string."
                return string_or_list
        else:
            print "[get_sth_unicode]The type of input varible is neither LIST or STRING."
            print "[get_sth_unicode]What it is:", string_or_list
            print "[get_sth_unicode]What it's type:", type(string_or_list)
            print '[get_sth_unicode]Return the special character:"".'
            string_or_list = ""
            return string_or_list



    def remove_sentence_stopwords_process(self, sentence_list, stopword_list):
        print "start remove sentence list stopwords process at " + time.strftime('%Y-%m-%d %X', time.localtime())
        remove_stopword_sentence_list = map(lambda sentence: self.remove_sentence_stopwords(sentence = sentence, stopword_list = stopword_list), sentence_list)
        print "len(remove_stopword_sentence_list):", len(remove_stopword_sentence_list)

        print "end remove sentence list stopwords process at " + time.strftime('%Y-%m-%d %X', time.localtime())
        return remove_stopword_sentence_list



    def remove_sentence_stopwords(self, sentence, stopword_list):
        cur_sentence = sentence
        for idx in xrange(len(stopword_list)):
            #print idx
            stopword = stopword_list[idx]
            try:
                while cur_sentence.find(stopword) != -1:
                    #print idx
                    cur_sentence = ''.join(cur_sentence.split(stopword))
            except:
                print "[remove_sentence_stopwords]sentence is None."
                continue
        remove_stopwords_sentence = cur_sentence
        return remove_stopwords_sentence


    def join_essays_title_and_content_into_list(self, essay_list):
        essays_joined_title_content_list = map(lambda essay: essay[1] + essay[2], essay_list)
        '''
        essays_joined_title_content_list = []
        for idx in xrange(len(essay_list)):
            essay = essay_list[idx]
            title_and_content = essay[1] + essay[2]
            essays_joined_title_content_list.append(title_and_content)
        '''
        return essays_joined_title_content_list



    def remove_blank_str_in_list(self, raw_list):
        return filter(lambda string: string != "", raw_list)



    def chinsese_segmentation_for_str_list(self, string_list, word_list):

        return map(lambda string: self.maximum_matching(sentence = string, word_list = word_list), string_list)



    def bidirectional_maximum_matching(self, sentence, word_list):

        mm_segmentation_reult_list = self.maximum_matching(sentence = sentence, word_list = word_list)
        rmm_segmentation_result_list = self.reverse_maximun_matching(sentence = sentence, word_list = word_list)

        print "MM:", len(mm_segmentation_reult_list)
        print "RMM:", len(rmm_segmentation_result_list)
        print
        if len(rmm_segmentation_result_list) <= len(mm_segmentation_reult_list):
            final_segmentation_result_list = rmm_segmentation_result_list
        else:
            final_segmentation_result_list = mm_segmentation_reult_list
        return final_segmentation_result_list



    def maximum_matching(self, sentence, word_list):
        segmentation_result_list = []
        try:
            while (len(sentence) > 0):
                for idx in range(len(word_list)):
                    word = word_list[idx]
                    if sentence[:len(word)] == word:
                        segmentation_result_list.append(word)
                        sentence = sentence[len(word):]

                    if idx == len(word_list)-1:
                        segmentation_result_list.append(sentence[:1])
                        sentence = sentence[1:]
        except:
            print "mm process terminate, sentence:%s." % sentence
        return segmentation_result_list



    def reverse_maximun_matching(self, sentence, word_list):
        reversed_sentence = sentence[::-1]
        reversed_word_list = map(lambda word: word[::-1], word_list)
        segmentation_result_list = self.maximum_matching(sentence = reversed_sentence, word_list = reversed_word_list)
        segmentation_result_list = map(lambda word: word[::-1], segmentation_result_list[::-1])
        return segmentation_result_list



    def word_frequency_statistic(self, essay_word_2d_list):
        """essay_word_list is a 2-D list"""
        essay_word_list = sum(sum(essay_word_2d_list, []), [])
        essay_word_set = set(essay_word_list)
        essay_word_dict = {}
        for word in essay_word_set:
            essay_word_dict[word] = 0

        for idx in xrange(len(essay_word_list)):
            word = essay_word_list[idx]
            essay_word_dict[word] += 1

        return essay_word_dict

################################### PART3 CLASS TEST ##################################
# initial parameters
word_database_name = "wordsDB"
word_table_name = "chinese_word_table"
essay_database_name = "essayDB"
essay_table_name = "securities_newspaper_shzqb_table"
sign_list = [".", "?", "!", "。", "，", "？", "！"]
'''
raw_string = "央行昨日逆回购500亿元。通过在公开市场展开逆回购来释放流动性，已成为近期央行操作常态。较低的中标利率，亦凸显央行引导资金利率运行中枢下行的意图。市场人士认为，控制和降低宏观及金融风险的有效举措之一，就是通过多种政策工具保证国内流动性充裕，将银行间市场利率维持在相对较低、平稳的水平。"
raw_string = test.get_string_or_list_unicode(raw_string)
print "raw_string:", raw_string
'''


test = ChineseWordSegmentation(database_name = word_database_name)
sign_list = test.get_string_or_list_unicode(sign_list)


# Get data of stopwords, words, essays from database.
stopword_list = test.get_sentence_stopword_list(database_name = word_database_name, table_name = word_table_name)
# essay_list is a 2D list.
essay_list = test.get_essay_list(database_name = essay_database_name, table_name = essay_table_name)
word_list = test.get_word_list(database_name = word_database_name, table_name = word_table_name)
word_list.sort(key=len, reverse = True)
#print "len(word_list)", len(word_list)
#for i in word_list[101:201]: print i


# pre-process.join essay's title and content into one string, split into sentences, remove stopwords.
# 1.join essay's title and content into one string,
essay_str_list = test.join_essays_title_and_content_into_list(essay_list = essay_list)
print "len(essay_str_list):", len(essay_str_list)
print "essay_str_list[0]:", essay_str_list[0]
print "len(essay_str_list[0]):", len(essay_str_list[0])
print "type(essay_str_list[0]):", type(essay_str_list[0])
# 2.split each essay string(title and content) into sentences.
# therefore, essay_str_sentence_list is a 2-D list variable.
essay_str_sentence_list = map(lambda essay_str: test.split_raw_string_into_sentence_process(raw_string = essay_str, sign_list = sign_list), essay_str_list)
print "len(essay_str_sentence_list)", len(essay_str_sentence_list)
print "essay_str_sentence_list[0]:", essay_str_sentence_list[0]
print "type(essay_str_sentence_list[0]):", type(essay_str_sentence_list[0])
print "len(essay_str_sentence_list[0]):", len(essay_str_sentence_list[0])
# 3.remove stopwords from  2-D list variable essay_str_sentence_list
# therefore, removed_stopwords_essay_str_sentence_list is a 2-D list variable, too.
removed_stopwords_essay_str_sentence_list = map(lambda essay_str_sentence_lis: test.remove_sentence_stopwords_process(sentence_list = essay_str_sentence_lis, stopword_list = stopword_list), essay_str_sentence_list)
print "removed_stopwords_essay_str_sentence_list[0]:", removed_stopwords_essay_str_sentence_list[0]
# 4.filter the blank string such as "".
# removed_blank_essay_str_sentence_list is a 2-D list variable.
removed_blank_essay_str_sentence_list = map(lambda essay_str_sentence_list: test.remove_blank_str_in_list(raw_list = essay_str_sentence_list), removed_stopwords_essay_str_sentence_list)
print "len(removed_blank_essay_str_sentence_list):", len(removed_blank_essay_str_sentence_list)
print "removed_blank_essay_str_sentence_list[0]:", removed_blank_essay_str_sentence_list[0]
print "type(removed_blank_essay_str_sentence_list[0]):", type(removed_blank_essay_str_sentence_list[0])
print "len(removed_blank_essay_str_sentence_list[0]):", len(removed_blank_essay_str_sentence_list[0])





raw_string = "IBM“Spark 部署及示例代码讲解”，本文介绍了如何下载、部署 Spark 及示例代码的运行。此外，深入介绍了运行代码的过程、脚本内容，通过这些介绍力求让读者可以快速地上手 Spark。"
raw_string = unicode(raw_string, "utf-8")
mm_split_result = test.maximum_matching(sentence = raw_string, word_list = word_list)
print "mm_split_result:", "|".join(mm_split_result)
rmm_split_result = test.reverse_maximun_matching(sentence = raw_string, word_list = word_list)
print "rmm_split_result:", "|".join(rmm_split_result)
final_split_result = test.bidirectional_maximum_matching(sentence = raw_string, word_list = word_list)
print "final_split_result:", "|".join(final_split_result)



# Make words segmentation.
# essay_segmentation_result_list is a 2D list.
print "start making words segmentation at " + time.strftime('%Y-%m-%d %X', time.localtime()) + "."
essay_segmentation_result_list = map(lambda sentence:test.bidirectional_maximum_matching(sentence = sentence, word_list = word_list), removed_stopwords_essay_str_sentence_list)
print "len(essay_segmentation_result_list):", len(essay_segmentation_result_list)
print "len(essay_segmentation_result_list[0]):", len(essay_segmentation_result_list[0])
print "essay_segmentation_result_list[0]:", essay_segmentation_result_list[0]
print "end making words segmentation at " + time.strftime('%Y-%m-%d %X', time.localtime()) + "."



# news record 3
essay_word_dict = test.word_frequency_statistic(essay_word_2d_list = essay_segmentation_result_list)
for key, value in essay_word_dict.items():
    print key, value
print "len(essay_word_dict):", len(essay_word_dict)
print essay_word_dict
