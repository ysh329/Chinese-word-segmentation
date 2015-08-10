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
import pandas as pd
import matplotlib.pyplot as plt

################################### PART2 CLASS && FUNCTION ###########################
class segmentation_result_analyser(object):
    def __init__(self):
        pass

    def __del__(self):
        pass

    def word_frequency_statistic(self, essay_word_2d_list):
        """essay_word_list is a 2-D list"""
        try:
            essay_word_2d_list = sum(sum(essay_word_2d_list, []), [])
        except:
            essay_word_2d_list = sum(essay_word_2d_list, [])
        finally:
            essay_word_set = set(essay_word_2d_list)

        word_list = map(lambda word: word, essay_word_set)
        word_dict = {}
        for word in word_list: word_dict[word] = 0
        for word in essay_word_2d_list:
            word_dict[word] += 1

        return word_dict

    def sort_dict(self, word_dict):
        sorted_word_tuple =  sorted(word_dict.items(), key=lambda d: d[1], reverse = True)
        return sorted_word_tuple
        # sort according to key
        #print sorted(dict1.items(), key=lambda d: d[0])
        # sort according to value
        #print sorted(dict1.items(), key=lambda d: d[1])

    def get_top_n_words(self, sorted_word_tuple, n = 10):
        if n >= len(sorted_word_tuple) or n < 1:
            print "input n is wrong, please try again."
            return
        else:
            print "sort by top %s words(according to 10 biggest show times)." % n
            top_n_words_tuple_list = sorted_word_tuple[:n]
        return top_n_words_tuple_list

    def show_top_n_words_dataframe(self, top_n_words_tuple_list):
        df = pd.DataFrame( [[ij for ij in i] for i in top_n_words_tuple_list] )
        df.rename(columns={0: 'word', 1: 'showtimes'}, inplace=True)
        df = df.sort(['showtimes'], ascending=False)
        print df.head()

    def show_top_n_words_plot(self, top_n_words_tuple_list, n):
        word_list = map(lambda tuple_word: tuple_word[0], top_n_words_tuple_list)
        showtimes_list = map(lambda tuple_word: tuple_word[1], top_n_words_tuple_list)

        num_bins = len(showtimes_list)
        #plt.hist(showtimes_list, num_bins, normed = 1, facecolor = 'green', alpha = 0.5)
        plt.bar(left = xrange(len(showtimes_list)), height = showtimes_list, width = .85, color = 'green')
        plt.title('Top %d words frequency' % n)
        plt.show()
################################### PART3 CLASS TEST ##################################
'''
Analyser = segmentation_result_analyser()
testlist = [['a', 'a', 'd', 'e'], ['a', 'b'], ['c','a', 'b', 'c'], ['b', 'b', 'c', 'a', 'b', 'c', 'a', 'b'], ['c']]
top_n = 4
#print testlist
word_dict = Analyser.word_frequency_statistic(essay_word_2d_list = testlist)
sorted_word_tuple = Analyser.sort_dict(word_dict = word_dict)
#print sorted_word_tuple
top_n_words_tuple_list = Analyser.get_top_n_words(sorted_word_tuple = sorted_word_tuple, n = top_n)
Analyser.show_top_n_words_dataframe(top_n_words_tuple_list = top_n_words_tuple_list)
Analyser.show_top_n_words_plot(top_n_words_tuple_list = top_n_words_tuple_list, n = top_n)
'''
# sort according to key
#print sorted(dict1.items(), key=lambda d: d[0])
# sort according to value
#print sorted(dict1.items(), key=lambda d: d[1])
