# -*- coding: utf-8 -*-
# !/usr/bin/python
################################### PART0 DESCRIPTION #################################
# Filename: main.py
# Description:
#        STEP1. (CLASS class_import_words_2_db.py)
#               Import words data from Sogou's cell words base and Chinese modern dictionary
#               to database 'wordsDB' table 'chinese_word_table'.
#        STEP2. (CLASS class_update_in_db.py)
#               Update or increase table's some fields, such as 'pinyin', 'meaning' fields, etc.
#        STEP3. (CLASS class_bidirectional_matching_algorithm.py)
#               Make Chinese word segmentation by MM and RMM methods.
#        STEP4. (CLASS class_segmentation_result_analyser.py)
#               Analise the result of Chinese word segmentation step, such as word frequency
#               statistic, result visualization, etc.

# Author: Shuai Yuan
# E-mail: ysh329@sina.com
# Create: 2015-8-10 17:52:03
# Last:
__author__ = 'yuens'
################################### PART1 IMPORT ######################################
from myclass.class_import_words_2_db import *
from myclass.class_update_in_db import *
from myclass.class_bidirectional_matching_algorithm import *
from myclass.class_segmentation_result_analyser import *
################################### PART2 MAIN && FUNCTION ############################
def main():
    # STEP1.(CLASS class_import_words_2_db.py)
    #       Import words data from Sogou's cell words base and Chinese modern dictionary
    #       to database 'wordsDB' table 'chinese_word_table'.
    # initial parameters
    database_name = "wordsDB"
    table_name = "chinese_word_table"
    general_words_file_dir = "../data/sogou_cellbase-utf8.txt"
    stopwords_base_dir = "../data/"

    WordsImporter = import_words_2_db()
    WordsImporter.create_database(database_name = database_name)
    WordsImporter.create_table(database_name= database_name, table_name = table_name)
    '''
    WordsImporter.insert_words_from_file_2_db(file_dir = general_words_file_dir, database_name = database_name, table_name = table_name)
    WordsImporter.insert_stopwords_from_file_2_db(file_dir = stopwords_base_dir, database_name = database_name, table_name = table_name)
    '''
    WordsImporter.insert_modern_chinese_dictionary_2_db(file_name = 'modern_chinese_dictionary.txt', database_name = database_name, table_name = table_name)



    # STEP2. (CLASS class_update_in_db.py)
    #        Update or increase table's some fields, such as 'pinyin', 'meaning' fields, etc.
    # initial parameters
    word_database_name = "wordsDB"

    Updator = update_in_db(database_name = word_database_name)



    # STEP3. (CLASS class_bidirectional_matching_algorithm.py)
    #        Make Chinese word segmentation by MM and RMM methods.
    # initial parameters
    word_database_name = "wordsDB"
    word_table_name = "chinese_word_table"
    essay_database_name = "essayDB"
    essay_table_name = "securities_newspaper_shzqb_table"
    sign_list = [".", "?", "!", "。", "，", "？", "！"]

    Segmentation = bidirectional_matching_algorithm(database_name = word_database_name)
    sign_list = Segmentation.get_string_or_list_unicode(sign_list)
    stopword_list = Segmentation.get_sentence_stopword_list(database_name = word_database_name, table_name = word_table_name)
    # news record 3!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    essay_list = Segmentation.get_essay_list(database_name = essay_database_name, table_name = essay_table_name)
    word_list = Segmentation.get_word_list(database_name = word_database_name, table_name = word_table_name)
    word_list.sort(key=len, reverse = True)

    essay_str_list = Segmentation.join_essays_title_and_content_into_list(essay_list = essay_list)
    essay_str_sentence_list = map(lambda essay_str: Segmentation.split_raw_string_into_sentence_process(raw_string = essay_str, sign_list = sign_list), essay_str_list)
    removed_stopwords_essay_str_sentence_list = map(lambda essay_str_sentence_lis: Segmentation.remove_sentence_stopwords_process(sentence_list = essay_str_sentence_lis, stopword_list = stopword_list), essay_str_sentence_list)
    removed_blank_essay_str_sentence_list = map(lambda essay_str_sentence_list: Segmentation.remove_blank_str_in_list(raw_list = essay_str_sentence_list), removed_stopwords_essay_str_sentence_list)
    # essay_segmentation_result_list is a 2-D list variable.
    essay_segmentation_result_list = map(lambda sentence: Segmentation.chinsese_segmentation_for_str_list(string_list = sentence, word_list = word_list), removed_blank_essay_str_sentence_list)



    # STEP4. (CLASS class_segmentation_result_analyser.py)
    #        Analise the result of Chinese word segmentation step, such as word frequency
    #        statistic, result visualization, etc.
    Analyser = segmentation_result_analyser()
    essay_word_dict = Analyser.word_frequency_statistic(essay_word_2d_list = essay_segmentation_result_list)
    sorted_essay_word_tuple = Analyser.sort_dict(word_dict = essay_word_dict)
    print 'sorted_essay_word_tuple:', sorted_essay_word_tuple
    top_n_words_tuple = Analyser.get_top_n_words(sorted_word_tuple = sorted_word_tuple, n = 3)
    print 'top_n_words_tuple:', top_n_words_tuple

################################ PART4 EXECUTE ##################################
if __name__ == "__main__":
    main()