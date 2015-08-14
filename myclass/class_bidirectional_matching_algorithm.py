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
import time
import logging
################################### PART2 CLASS && FUNCTION ###########################
class bidirectional_matching_algorithm(object):
    def __init__(self, database_name):
        """ Initialize a entry of class.
        Args:
            database_name (str): input database name
        Returns:
            None
        """
        self.start = time.clock()
        logging.basicConfig(level = logging.DEBUG,
                  format = '%(asctime)s  %(filename)19s[line:%(lineno)3d]  %(levelname)5s  %(message)s',
                  datefmt = '%y-%m-%d %H:%M:%S',
                  filename = '../main.log',
                  filemode = 'a')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s  %(filename)19s[line:%(lineno)3d]  %(levelname)5s  %(message)s')
        console.setFormatter(formatter)

        logging.getLogger('').addHandler(console)
        logging.info("[bidirectional_matching_algorithm][__init__]START at " + time.strftime('%Y-%m-%d %X', time.localtime()))

        try:
            self.con = MySQLdb.connect(host = "localhost", user = "root", passwd = "931209", db = database_name, charset = "utf8")
            logging.info("[bidirectional_matching_algorithm][__init__]Connected MySQL successfully.")
        except MySQLdb.Error, e:
            logging.error("[bidirectional_matching_algorithm][__init__]Failed in connecting database %s." % database_name)
            logging.error("[bidirectional_matching_algorithm][__init__]MySQL Error %d: %s." % (e.args[0], e.args[1]))



    def __del__(self):
        """ Delete a entry of class.
        Args:
            None
        Returns:
            None
        """
        self.end = time.clock()
        self.con.close()
        logging.info("[bidirectional_matching_algorithm][__del__]Elapsed time:%0.3f" % (self.end - self.start))
        logging.info("[bidirectional_matching_algorithm][__del__]End at:" + time.strftime('%Y-%m-%d %X', time.localtime()))



    def split_raw_string_into_sentence_process(self, raw_string, sign_list):
        """ Split a raw string into sentence according to symbol in this raw string for multi-strings.
        Args:
            raw_string (str): a string prepared to be split.
            sign_list  (list): a list contain all the symbols such as , . ! ? etc. which are used to break a sentence.
        Returns:
            sentence_list (list): a list that contain the split result for raw string according to the symbol in it.
        """
        logging.info("[bidirectional_matching_algorithm][split_raw_string_into_sentence_process]Start pre process at " + time.strftime('%Y-%m-%d %X', time.localtime()))
        reversed_split_index_list = map(lambda sign: self.find_index(raw_string = raw_string, sign = sign), sign_list)
        reversed_split_index_list = list( sorted(set(sum(reversed_split_index_list, [])), reverse=True) )
        logging.info("[bidirectional_matching_algorithm][split_raw_string_into_sentence_process]len(reversed_split_index_list):" % len(reversed_split_index_list))

        sentence_list = self.split_raw_string_into_sentence_list(raw_string = raw_string, reversed_split_index_list = reversed_split_index_list)
        logging.info("[bidirectional_matching_algorithm][split_raw_string_into_sentence_process]len(sentence_list):" % len(sentence_list))

        logging.info("[bidirectional_matching_algorithm][split_raw_string_into_sentence_process]End pre process at " + time.strftime('%Y-%m-%d %X', time.localtime()))
        return sentence_list



    def find_index(self, raw_string, sign):
        """ Find the index of symbol in the raw string.
        Args:
            raw_string (str): a string prepared to be split.
            sign       (str): a symbol used to break the raw string. The symbol may be , . ? ! etc.
                             (English mode or Chinese mode).
        Returns:
            index_list (list): a list that contain the index for raw string according to the symbol in it.
        """
        cur_string = raw_string
        index_list = []
        for idx in xrange(raw_string.count(sign)):
            index = cur_string.rfind(sign)
            index_list.append(index)
            cur_string = cur_string[:index]
        return index_list



    def split_raw_string_into_sentence_list(self, raw_string, reversed_split_index_list):
        """ Split a raw string into sentence list for one string.
        Args:
            raw_string (str): a string prepared to be split.
            reversed_split_index_list (list): a index list for raw string about all symbols (sign_list).
        Returns:
            sentence_list (list): a list that contain split result for raw string according to symbol
                                  index in raw string..
        """
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
        return sentence_list



    def get_essay_list(self, database_name, table_name):
        """ Get title and content of essays from one table of database 'essayDB'.
        Args:
            database_name (str): a string contained the name of essay database.
            table_name    (str): a string contained the name of essay table.
        Returns:
            essay_list   (list): a 2-D list that contain each essays' id, title and content.
        """
        essay_list = []
        cursor = self.con.cursor()
        try:
            sql = """SELECT id, title, content FROM %s.%s""" % (database_name, table_name)
            cursor.execute(sql)
            essay_tuple = cursor.fetchall()
            logging.info("[bidirectional_matching_algorithm][get_essay_list]len(essay_tuple):", len(essay_tuple))
            logging.info("[bidirectional_matching_algorithm][get_essay_list]type(essay_tuple):", type(essay_tuple))
            logging.info("[bidirectional_matching_algorithm][get_essay_list]essay_tuple[0]:", essay_tuple[0])
            logging.info("[bidirectional_matching_algorithm][get_essay_list]len(essay_tuple[0]):", len(essay_tuple[0]))
            logging.info("[bidirectional_matching_algorithm][get_essay_list]type(essay_tuple[0]):", type(essay_tuple[0]))
            logging.info("[bidirectional_matching_algorithm][get_essay_list]essay_tuple[0][0]:", essay_tuple[0][0])
            logging.info("[bidirectional_matching_algorithm][get_essay_list]essay_tuple[0][1]:", essay_tuple[0][1])
            logging.info("[bidirectional_matching_algorithm][get_essay_list]essay_tuple[0][2]:", essay_tuple[0][2])
            logging.info("[bidirectional_matching_algorithm][get_essay_list]type(essay_tuple[0][1]):", type(essay_tuple[0][1]))

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
                        logging.error("[bidirectional_matching_algorithm][get_essay_list]Transform encoding to unicode failed.")
                        logging.error("[bidirectional_matching_algorithm][get_essay_list]essay_tuple[0][0]:", essay_tuple[0][0])
                        logging.error("[bidirectional_matching_algorithm][get_essay_list]essay_tuple[0][1]:", essay_tuple[0][1])
                        logging.error("[bidirectional_matching_algorithm][get_essay_list]essay_tuple[0][2]:", essay_tuple[0][2])
                        continue
        except MySQLdb.Error, e:
            logging.error("[bidirectional_matching_algorithm][get_essay_list]Failed in selecting stopwords from table %s database %s." % (table_name, database_name))
            logging.error("[bidirectional_matching_algorithm][get_essay_list]MySQL Error %d: %s." % (e.args[0], e.args[1]))

        logging.info("[bidirectional_matching_algorithm][get_essay_list]Get essay list successfully.")
        logging.info("[bidirectional_matching_algorithm][get_essay_list]Get essay record %s." % (len(essay_list)))
        return essay_list



    def get_word_list(self, database_name, table_name):
        """ Get word list from one table of database 'wordsDB'.
        Args:
            database_name (str): a string contained the name of word database.
            table_name    (str): a string contained the name of word table.
        Returns:
            word_list   (list): a list that contain each word..
        """
        word_list = []

        cursor = self.con.cursor()
        try:
            sql = """SELECT word FROM %s.%s WHERE type1='t1'""" % (database_name, table_name)
            cursor.execute(sql)
            word_tuple = cursor.fetchall()
            if len(word_tuple) > 0:
                for idx in xrange(len(word_tuple)):
                    try:
                        word = word_tuple[idx][0]
                        if type(word) != unicode: word = unicode(word, "utf8")
                        word_list.append(word)
                    except:
                        logging.error("[bidirectional_matching_algorithm][get_word_list]Failed in transforming word %s to unicode form." % word)
                        logging.error("[bidirectional_matching_algorithm][get_word_list]word %s %s" % (word, type(word)))
                        continue
            logging.info("[bidirectional_matching_algorithm][get_word_list]get words %s from database successfully." % len(word_list))
        except MySQLdb.Error, e:
            logging.error("[bidirectional_matching_algorithm][get_word_list]Failed in selecting words from database %s." % database_name)
            logging.error("[bidirectional_matching_algorithm][get_word_list]MySQL Error %d: %s." % (e.args[0], e.args[1]))
        return word_list



    def get_sentence_stopword_list(self, database_name, table_name):
        """ Get stopword list from table 'chinese_word_table' of database 'wordsDB'.
        Args:
            database_name (str): a string contained the name of word database 'wordsDB'.
            table_name    (str): a string contained the name of word table 'chinese_word_table'.
        Returns:
            stopword_list (list): a list that contain each stopword.
        """
        stopword_list = [] # unicode stopword

        cursor = self.con.cursor()
        try:
            sql = """SELECT word FROM %s.%s WHERE type1='stopword'""" % (database_name, table_name)
            cursor.execute(sql)
            stopword_tuple = cursor.fetchall()
            logging.info("[bidirectional_matching_algorithm][get_sentence_stopword_list]len(stopword_tuple):", len(stopword_tuple))
            logging.info("[bidirectional_matching_algorithm][get_sentence_stopword_list]type(stopword_tuple):", type(stopword_tuple))
            logging.info("[bidirectional_matching_algorithm][get_sentence_stopword_list]stopword_tuple[0]:", stopword_tuple[0])
            logging.info("[bidirectional_matching_algorithm][get_sentence_stopword_list]stopword_tuple[0][0]:", stopword_tuple[0][0])
            logging.info("[bidirectional_matching_algorithm][get_sentence_stopword_list]type(stopword_tuple[0][0]):", type(stopword_tuple[0][0]))
            if len(stopword_tuple) > 0:
                for idx in xrange(len(stopword_tuple)):
                    try:
                        stopword = stopword_tuple[idx][0]
                        if type(stopword) != unicode: stopword = unicode(stopword, "utf8")
                        stopword_list.append(stopword)
                    except:
                        logging.error("[bidirectional_matching_algorithm][get_sentence_stopword_list]Failed in transforming stopword %s to unicode form." % stopword_tuple[idx][0])
                        logging.error("[bidirectional_matching_algorithm][get_sentence_stopword_list]stopword %s %s" % (stopword, type(stopword)))
                        continue
            logging.info("[bidirectional_matching_algorithm][get_sentence_stopword_list]Get stopwords %s from database successfully." % len(stopword_list))
        except MySQLdb.Error, e:
            logging.error("[bidirectional_matching_algorithm][get_sentence_stopword_list]Failed in selecting stopwords from database %s." % database_name)
            logging.error("[bidirectional_matching_algorithm][get_sentence_stopword_list]MySQL Error %d: %s." % (e.args[0], e.args[1]))
        return stopword_list



    def get_string_or_list_unicode(self, string_or_list):
        """ Get a new string or list in a unicode form, transform a list of strings or a string
        into a unicode 'utf8' form.
        Args:
            string_or_list (str or list): a string or a list of string.
        Returns:
            string_or_list (unicode or list): a list that contain each string(unicode utf8) or a
        unicode string.
        """
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
                        logging.error("[bidirectional_matching_algorithm][get_string_or_list_unicode]The element of list's type is not UFT8.")
                        logging.error("[bidirectional_matching_algorithm][get_string_or_list_unicode]What it is:", string_or_list[i])
                        logging.error("[bidirectional_matching_algorithm][get_string_or_list_unicode]What it's type:", type(string_or_list[i]))
                        logging.error("[bidirectional_matching_algorithm][get_string_or_list_unicode]Ignore this element in list(continue execute).")
                        continue
            return unicode_list
        elif type(string_or_list) == str:
            try:
                unicode_string = unicode(string_or_list, "utf8")
                return unicode_string
            except:
                logging.error("[bidirectional_matching_algorithm][get_string_or_list_unicode]The string's type is not utf8.")
                logging.error("[bidirectional_matching_algorithm][get_string_or_list_unicode]OR the string's type is UNICODE.")
                logging.error("[bidirectional_matching_algorithm][get_string_or_list_unicode]Return original string.")
                return string_or_list
        else:
            logging.error("[bidirectional_matching_algorithm][get_string_or_list_unicode]The type of input varible is neither LIST or STRING.")
            logging.error("[bidirectional_matching_algorithm][get_string_or_list_unicode]What it is:", string_or_list)
            logging.error("[bidirectional_matching_algorithm][get_string_or_list_unicode]What it's type:", type(string_or_list))
            logging.error("[bidirectional_matching_algorithm][get_string_or_list_unicode]Return the special character:''.")
            string_or_list = ""
            return string_or_list



    def remove_sentence_stopwords_process(self, sentence_list, stopword_list):
        """ Remove sentences(sentence list)'s stopword.
        Args:
            sentence_list (list): a list of strings.
            stopword_list (list): a list that contain all the stopword from table
        "chinese_word_table" of database "wordsDB".
        Returns:
            remove_stopword_sentence_list (2-D list): sentence list that each sentence
        string doesn't contain stopword.
        """
        logging.info("[bidirectional_matching_algorithm][remove_sentence_stopwords_process]Start remove sentence list stopwords process at " + time.strftime('%Y-%m-%d %X', time.localtime()))
        remove_stopword_sentence_list = map(lambda sentence: self.remove_sentence_stopwords(sentence = sentence, stopword_list = stopword_list), sentence_list)
        logging.info("[bidirectional_matching_algorithm][remove_sentence_stopwords_process]len(remove_stopword_sentence_list):", len(remove_stopword_sentence_list))
        logging.info("[bidirectional_matching_algorithm][remove_sentence_stopwords_process]End remove sentence list stopwords process at " + time.strftime('%Y-%m-%d %X', time.localtime()))
        return remove_stopword_sentence_list



    def remove_sentence_stopwords(self, sentence, stopword_list):
        """ Remove sentence's all stopwords.
        Args:
            sentence      (str): a string.
            stopword_list (list): a list that contain all the stopwords from
        "chinese_word_table" of database "wordsDB".
        Returns:
            remove_stopword_sentence_list (2-D list): sentence list that each sentence
        string doesn't contain stopword.
        """
        cur_sentence = sentence
        for idx in xrange(len(stopword_list)):
            stopword = stopword_list[idx]
            try:
                while cur_sentence.find(stopword) != -1:
                    cur_sentence = ''.join(cur_sentence.split(stopword))
            except:
                logging.error("[bidirectional_matching_algorithm][remove_sentence_stopwords]sentence is None.")
                continue
        remove_stopwords_sentence = cur_sentence
        return remove_stopwords_sentence



    def join_essays_title_and_content_into_list(self, essay_list):
        """ Join each essay's title and content into one string.
        Args:
            essay_list    (2-D list): a 2-D list, each element is a
        list contained essay id, title, content.
        Returns:
            essays_joined_title_content_list (list): a list, each
        element is one essay's representation of its title and content
        joined string.
        """
        essays_joined_title_content_list = map(lambda essay: essay[1] + essay[2], essay_list)
        return essays_joined_title_content_list



    def remove_blank_str_in_list(self, raw_list):
        """ Remove blank string in a list(each element is a string).
        Args:
            raw_list    (list): a list contain string elements.
        Returns:
            a list doesn't contain blank string.
        """
        return filter(lambda string: string != "", raw_list)



    def chinese_segmentation_for_str_list(self, string_list, word_list):
        """ Adopt chinese segmentation of maximum matching method for
        strings(list).
        Args:
            string_list  (list): a list contain string elements(each element is
        a sentence/string).
            word_list    (list): a list contain words used for chinese word
        segmentation.
        Returns:
            a 3-D list contains the result of chinese segmentation.
        """
        return map(lambda string: self.maximum_matching(sentence = string, word_list = word_list), string_list)



    def bidirectional_maximum_matching(self, sentence, word_list):
        """ Adopt chinese segmentation of bidirectional maximum matching(maximum matching
         and reverse maximum matching) method, which will select a better one in these two
         methods for (sentence) string.
        Args:
            sentence     (str): a sentence used for chinese segmentation of bidirectional
        maximum matching.
            word_list    (list): a list contain words used for chinese word segmentation.
        Returns:
            final_segmentation_result_list  (list): a list contains chinese segmentation
        result.
        """
        mm_segmentation_reult_list = self.maximum_matching(sentence = sentence, word_list = word_list)
        rmm_segmentation_result_list = self.reverse_maximun_matching(sentence = sentence, word_list = word_list)
        logging.info("[bidirectional_matching_algorithm][remove_sentence_stopwords]MM:", len(mm_segmentation_reult_list), "RMM:", len(rmm_segmentation_result_list))
        if len(rmm_segmentation_result_list) <= len(mm_segmentation_reult_list):
            final_segmentation_result_list = rmm_segmentation_result_list
        else:
            final_segmentation_result_list = mm_segmentation_reult_list
        return final_segmentation_result_list



    def maximum_matching(self, sentence, word_list):
        """ Adopt chinese segmentation of maximum matching method for (sentence) string.
        Args:
            sentence     (str): a sentence used for chinese segmentation of bidirectional
        maximum matching.
            word_list    (list): a list contain words used for chinese word segmentation.
        Returns:
            segmentation_result_list  (list): a list contains chinese segmentation result.
        """
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
            logging.error("[bidirectional_matching_algorithm][remove_sentence_stopwords]MM process terminate, sentence:%s." % sentence)
        return segmentation_result_list



    def reverse_maximun_matching(self, sentence, word_list):
        """ Adopt chinese segmentation of reverse maximum matching method(based on maximum
        matching) for (sentence) string.
        Args:
            sentence     (str): a sentence used for chinese segmentation of bidirectional
        maximum matching.
            word_list    (list): a list contain words used for chinese word segmentation.
        Returns:
            segmentation_result_list  (list): a list contains chinese segmentation result.
        """
        reversed_sentence = sentence[::-1]
        reversed_word_list = map(lambda word: word[::-1], word_list)
        segmentation_result_list = self.maximum_matching(sentence = reversed_sentence, word_list = reversed_word_list)
        segmentation_result_list = map(lambda word: word[::-1], segmentation_result_list[::-1])
        return segmentation_result_list



    def word_frequency_statistic(self, essay_word_2d_list):
        """ flatten the essay_word_2d_list(contain chinese segmentation result, it's a 3-D list in
         reality) twice to be a 1-D list(essay_word_list), which contains words. By using SET
         operation, we get the unique words as the word dictionary(word_dict, a key-value form).
         After that, we make statistic on all essays' words(essay_word_list).
        Args:
            essay_word_2d_list  (3-D list): result of chinese segmentation of bidirectional, a 3-D
         list.
        Returns:
            word_dict           (dict): store the result of word frequency statistic, key-value form.
        """
        essay_word_list = sum(sum(essay_word_2d_list, []), [])
        essay_word_set = set(essay_word_list)
        word_list = map(lambda word: word, essay_word_set)

        word_dict = {}
        for word in word_list: word_dict[word] = 0
        for word in essay_word_list:
            word_dict[word] += 1

        return word_dict
################################### PART3 CLASS TEST ##################################
'''
# initial parameters
word_database_name = "wordsDB"
word_table_name = "chinese_word_table"
essay_database_name = "essayDB"
essay_table_name = "securities_newspaper_shzqb_table"
sign_list = [".", "?", "!", "。", "，", "？", "！"]

test = bidirectional_matching_algorithm(database_name = word_database_name)
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

# Make words segmentation.
# essay_segmentation_result_list is a 2D list.
print "start making words segmentation at " + time.strftime('%Y-%m-%d %X', time.localtime()) + "."
essay_segmentation_result_list = map(lambda sentence: test.chinese_segmentation_for_str_list(string_list = sentence, word_list = word_list), removed_stopwords_essay_str_sentence_list)
print "len(essay_segmentation_result_list):", len(essay_segmentation_result_list)
print "len(essay_segmentation_result_list[0]):", len(essay_segmentation_result_list[0])
print "essay_segmentation_result_list[0]:", essay_segmentation_result_list[0]
print "end making words segmentation at " + time.strftime('%Y-%m-%d %X', time.localtime()) + "."

essay_word_dict = test.word_frequency_statistic(essay_word_2d_list = essay_segmentation_result_list)
print essay_word_dict
for word in essay_word_dict: print word, essay_word_dict[word]
'''



'''
raw_string = "IBM“Spark 部署及示例代码讲解”，本文介绍了如何下载、部署 Spark 及示例代码的运行。此外，深入介绍了运行代码的过程、脚本内容，通过这些介绍力求让读者可以快速地上手 Spark。"
raw_string = unicode(raw_string, "utf-8")
mm_split_result = test.maximum_matching(sentence = raw_string, word_list = word_list)
print "mm_split_result:", "|".join(mm_split_result)
rmm_split_result = test.reverse_maximun_matching(sentence = raw_string, word_list = word_list)
print "rmm_split_result:", "|".join(rmm_split_result)
final_split_result = test.bidirectional_maximum_matching(sentence = raw_string, word_list = word_list)
print "final_split_result:", "|".join(final_split_result)
'''
