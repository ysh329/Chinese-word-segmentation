# -*- coding: utf-8 -*-
# !/usr/bin/python
################################### PART0 DESCRIPTION #################################
# Filename: class_segmentation_result_analyser.py
# Description: Analise the result of Chinese word segmentation step, such as word frequency
#           statistic, result visualization, etc.

# Author: Shuai Yuan
# E-mail: ysh329@sina.com
# Create: 2015-8-10 18:47:07
# Last:
__author__ = 'yuens'
################################### PART1 IMPORT ######################################
import pandas
import matplotlib.pyplot as plt
import numpy as np
import logging
import time
################################### PART2 CLASS && FUNCTION ###########################
class segmentation_result_analyser(object):
    def __init__(self):
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
        logging.info("[segmentation_result_analyser][__init__]START at " + time.strftime('%Y-%m-%d %X', time.localtime()))



    def __del__(self):
        """ Delete a entry of class.
        Args:
            None
        Returns:
            None
        """
        self.stop = time.clock()
        logging.info("[segmentation_result_analyser][__del__]The class run time is : %.03f seconds" % (self.stop - self.start))
        logging.info("[segmentation_result_analyser][__del__]END at:" + time.strftime('%Y-%m-%d %X', time.localtime()))



    def word_frequency_statistic(self, essay_word_2d_list):
        """ Make words frequency statistic according the word list(essay_word_2d_list).
         Return a key-value form dictionary contained all unique words in word list(essay_word_2d_list),
         and it's a key-value form, which means key is the word, value is the frequency.
        Args:
            essay_word_2d_list  (2-D list): the essay's list, which has made the chinese word segmentation,
         it only has chinese words in 2-D list form.
        Returns:
            word_dict           (dict): A dictionary contains all unique words in essay_word_2d_list,
         which is a key-value form(key: word, value: word frequency).
        """
        try:
            essay_word_2d_list = sum(sum(essay_word_2d_list, []), [])
        except:
            pass
            #essay_word_2d_list = sum(essay_word_2d_list, [])
        finally:
            essay_word_set = set(essay_word_2d_list)

        word_list = map(lambda word: word, essay_word_set)
        word_dict = {}
        for word in word_list: word_dict[word] = 0
        for word in essay_word_2d_list:
            word_dict[word] += 1
        logging.info("[segmentation_result_analyser][word_frequency_statistic]finished frequency statistic task of words. words summation:%s(contains the words that don't exist in modern Chinese dictionary)" % len(word_dict))
        return word_dict



    def sort_dict(self, word_dict):
        """ Sort the dictionary(word_dict) according to the word frequency value of the word.
        Args:
            word_dict                (dict): A dictionary contains all unique words in
         essay_word_2d_list, which is a key-value form(key: word, value: word frequency).
        Returns:
            sorted_word_tuple_list   (list): A list, its elements is tuple(has 2 elements),
         1st element is word, 2rd one is value, and the tuple index in list is the word
         frequency rank(descending according to word frequency) in list.
        """
        sorted_word_tuple_list =  sorted(word_dict.items(), key=lambda d: d[1], reverse = True)
        logging.info("[segmentation_result_analyser][sort_dict]finished sort task of word dictionary.")
        return sorted_word_tuple_list
        # sort according to key
        #print sorted(dict1.items(), key=lambda d: d[0])
        # sort according to value
        #print sorted(dict1.items(), key=lambda d: d[1])



    def get_top_n_words(self, sorted_word_tuple_list, n = 10):
        """ Get top n words according to the word frequency previously variable
         (sorted_word_tuple_list, descending ranked).
        Args:
            sorted_word_tuple_list   (list): A list, its elements is tuple(has 2 elements),
         1st element is word, 2rd one is value, and the tuple index in list is the word
         frequency rank(descending according to word frequency) in list.
            n                        (int): top n words, the n value.
        Returns:
            top_n_words_tuple_list   (list): A list, its elements is tuple(has 2 elements),
         first element is word, second one is value, and the tuple index in list is the word
         frequency rank(descending according to word frequency) in list. It only has the top
         n tuple elements(according to word frequency ranked, second element in tuple).
        """
        if n >= len(sorted_word_tuple_list) or n < 1:
            logging.error("[segmentation_result_analyser][get_top_n_words]input n is wrong, please try again.")
            return
        else:
            logging.info("[segmentation_result_analyser][get_top_n_words]sort by top %s words(biggest showtimes/frequency)." % n)
            top_n_words_tuple_list = sorted_word_tuple_list[:n]
        return top_n_words_tuple_list



    def show_top_n_words_dataframe(self, top_n_words_tuple_list):
        """ Show top n words's frequency according to the word frequency in pandas
         library's DataFrame form.
        Args:
            top_n_words_tuple_list   (list): A list, its elements is tuple(has 2 elements),
         first element is word, second one is value, and the tuple index in list is the word
         frequency rank(descending according to word frequency) in list. It only has the top
         n tuple elements(according to word frequency ranked, second element in tuple).
        Returns:
            None
        """
        df = pandas.DataFrame( [[ij for ij in i] for i in top_n_words_tuple_list] )
        df.rename(columns={0: 'word', 1: 'showtimes'}, inplace = True)
        df = df.sort(['showtimes'], ascending = False)
        #print df.head()
        logging.info("[segmentation_result_analyser][get_top_n_words]df.head():%s" % str(df.head()))



    def show_top_n_words_plot(self, top_n_words_tuple_list, n):
        """ Plot top n words's frequency bar chart according to the word frequency in pandas
        library's DataFrame form.
        Args:
            top_n_words_tuple_list   (list): A list, its elements is tuple(has 2 elements),
         first element is word, second one is value, and the tuple index in list is the word
         frequency rank(descending according to word frequency) in list. It only has the top
         n tuple elements(according to word frequency ranked, second element in tuple).
            n                        (int): top n words, the n value.
        Returns:
            None
        """
        logging.info("[segmentation_result_analyser][show_top_n_words_plot]")
        word_list = map(lambda tuple_word: tuple_word[0], top_n_words_tuple_list)
        showtimes_list = map(lambda tuple_word: tuple_word[1], top_n_words_tuple_list)
        #std_showtimes = np.std(np.array(showtimes_list))

        index = np.arange(n)
        plt.xlabel('Words')
        plt.ylabel('Frequency')
        plt.ylim(0.0, max(showtimes_list) + 0.3*max(showtimes_list))
        plt.title('Top %d words frequency' % n)
        bar_width = 0.5
        plt.xticks(index + bar_width, word_list)
        bar_entry = plt.bar(left = xrange(len(showtimes_list)),
                height = showtimes_list,
                width = .85,
                alpha = 0.4, # bar opacity
                color = 'b',
                label = 'Word Frequency')
        plt.legend(bar_entry, ['Word Frequency'], 'best')
        plot_save_directory = "./data/output/result.png"
        plt.savefig(plot_save_directory, dpi = 78)



################################### PART3 CLASS TEST ##################################
'''
Analyser = segmentation_result_analyser()
testlist = [['a','z','c','d','f','g','k','e','y','e','y','e','y','e','y', 'f','g','k','f','g','k','a','a' 'a', 'd', 'e', 'a', 'b', 'c','a', 'b', 'c', 'b', 'b', 'c', 'a', 'b', 'c', 'a'], ['b', 'c']]
top_n = len(set(sum(testlist, [])))-1
#print testlist
word_dict = Analyser.word_frequency_statistic(essay_word_2d_list = testlist)
sorted_word_tuple_list = Analyser.sort_dict(word_dict = word_dict)
#print sorted_word_tuple_list
top_n_words_tuple_list = Analyser.get_top_n_words(sorted_word_tuple_list = sorted_word_tuple_list, n = top_n)
Analyser.show_top_n_words_dataframe(top_n_words_tuple_list = top_n_words_tuple_list)
Analyser.show_top_n_words_plot(top_n_words_tuple_list = top_n_words_tuple_list, n = top_n)
'''