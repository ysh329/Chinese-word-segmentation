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
#        STEP5. (CLASS class_update_in_db.py)
#               According to word frequency statistic result of essays, insert the statistic result in our essays
#               (or we can also call them corpus) to field 'showtimes' of data table 'chinese_word_table'.

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
    logging.basicConfig(level = logging.DEBUG,
              format = '%(asctime)s  %(filename)19s[line:%(lineno)3d]  %(levelname)5s  %(message)s',
              datefmt = '%y-%m-%d %H:%M:%S',
              filename = './main.log',
              filemode = 'a')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s  %(filename)19s[line:%(lineno)3d]  %(levelname)5s  %(message)s')
    console.setFormatter(formatter)

    logging.getLogger('').addHandler(console)
    logging.info("[main]START at " + time.strftime('%Y-%m-%d %X', time.localtime()))
    '''
    # STEP1.(CLASS class_import_words_2_db.py)
    #       Import words data from Sogou's cell words base and Chinese modern dictionary
    #       to database 'wordsDB' table 'chinese_word_table'.
    # initial parameters
    word_database_name = "wordsDB"
    word_table_name = "chinese_word_table"
    general_words_file_dir = "./data/sogou_cellbase-utf8.txt"
    stopwords_base_dir = "./data/"
    modern_chinese_dictionary_file_name = 'modern_chinese_dictionary.txt'

    WordsImporter = import_words_2_db()
    WordsImporter.create_database(database_name = word_database_name)
    WordsImporter.create_table(database_name= word_database_name, table_name = word_table_name)

    #WordsImporter3.insert_words_from_file_2_db(file_dir = general_words_file_dir, database_name = database_name, table_name = table_name)
    #WordsImporter.insert_stopwords_from_file_2_db(file_dir = stopwords_base_dir, database_name = database_name, table_name = table_name)

    WordsImporter.insert_modern_chinese_dictionary_2_db(file_name = modern_chinese_dictionary_file_name, database_name = word_database_name, table_name = word_table_name)
    '''
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
    essay_table_name1 = "securities_newspaper_shzqb_table"
    essay_table_name2 = "securities_newspaper_zgzqb_table"
    essay_table_name3 = "securities_newspaper_zqrb_table"
    essay_table_name4 = "securities_newspaper_zqsb_table"
    sign_list = [".", "?", "!", "。", "，", "？", "！"]

    Segmentation = bidirectional_matching_algorithm(database_name = word_database_name)
    sign_list = Segmentation.get_string_or_list_unicode(sign_list)

    essay_list1 = Segmentation.get_essay_list(database_name = essay_database_name, table_name = essay_table_name1)
    essay_str_list1 = Segmentation.join_essays_title_and_content_into_list(essay_list = essay_list1)
    essay_list2 = Segmentation.get_essay_list(database_name = essay_database_name, table_name = essay_table_name2)
    essay_str_list2 = Segmentation.join_essays_title_and_content_into_list(essay_list = essay_list2)
    essay_list3 = Segmentation.get_essay_list(database_name = essay_database_name, table_name = essay_table_name3)
    essay_str_list3 = Segmentation.join_essays_title_and_content_into_list(essay_list = essay_list3)
    essay_list4 = Segmentation.get_essay_list(database_name = essay_database_name, table_name = essay_table_name4)
    essay_str_list4 = Segmentation.join_essays_title_and_content_into_list(essay_list = essay_list4)
    essay_str_list = []
    essay_str_list.extend(essay_str_list1)
    essay_str_list.extend(essay_str_list2)
    essay_str_list.extend(essay_str_list3)
    essay_str_list.extend(essay_str_list4)

    #stopword_list = Segmentation.get_sentence_stopword_list(database_name = word_database_name, table_name = word_table_name)

    word_list = Segmentation.get_word_list(database_name = word_database_name, table_name = word_table_name)
    word_list.sort(key=len, reverse = True)
    '''
    # [TEST]
    print "len(essay_str_list):", len(essay_str_list)
    print "essay_str_list[0]:", essay_str_list[0]
    print "type(essay_str_list[0]):", type(essay_str_list[0])
    '''
    '''
    # [VERSION 1] Keep the part of removing stopwords.
    essay_str_sentence_list = map(lambda essay_str: Segmentation.split_raw_string_into_sentence_process(raw_string = essay_str, sign_list = sign_list), essay_str_list)
    removed_stopwords_essay_str_sentence_list = map(lambda essay_str_sentence_lis: Segmentation.remove_sentence_stopwords_process(sentence_list = essay_str_sentence_lis, stopword_list = stopword_list), essay_str_sentence_list)
    removed_blank_essay_str_sentence_list = map(lambda essay_str_sentence_list: Segmentation.remove_blank_str_in_list(raw_list = essay_str_sentence_list), removed_stopwords_essay_str_sentence_list)
    # essay_segmentation_result_list is a 2-D list variable.
    essay_segmentation_result_list = map(lambda sentence: Segmentation.chinese_segmentation_for_str_list(string_list = sentence, word_list = word_list), removed_blank_essay_str_sentence_list)
    '''
    # [VERSION 2] Dont keep the part of removing stopwords.
    # essay_str_sentence_list: 2-D list
    essay_str_sentence_list = map(lambda essay_str: Segmentation.split_raw_string_into_sentence_process(raw_string = essay_str, sign_list = sign_list), essay_str_list)
    '''
    # [TEST]
    print "len(essay_str_sentence_list):", len(essay_str_sentence_list)
    print "essay_str_sentence_list[0]:", essay_str_sentence_list[0]
    print "type(essay_str_sentence_list[0]):", type(essay_str_sentence_list[0])
    for stc in essay_str_sentence_list[0]: print stc
    '''
    essay_segmentation_result_list = map(lambda sentence: Segmentation.chinese_segmentation_for_str_list(string_list = sentence, word_list = word_list), essay_str_sentence_list)
    '''
    # [TEST]
    print "len(essay_segmentation_result_list):", len(essay_segmentation_result_list)
    print "essay_segmentation_result_list[0]:", essay_segmentation_result_list[0]
    print "type(essay_segmentation_result_list[0]):", type(essay_segmentation_result_list[0])
    essay_words_list = sum(sum(essay_segmentation_result_list, []), [])
    for word in essay_words_list: print word
    '''



    # STEP4. (CLASS class_segmentation_result_analyser.py)
    #        Analise the result of Chinese word segmentation step, such as word frequency
    #        statistic, result visualization, etc.
    Analyser = segmentation_result_analyser()
    top_n = 20

    essay_word_dict = Analyser.word_frequency_statistic(essay_word_2d_list = essay_segmentation_result_list)
    sorted_essay_word_tuple = Analyser.sort_dict(word_dict = essay_word_dict)
    logging.info("sorted_essay_word_tuple[:10]:", sorted_essay_word_tuple[:10])
    top_n_words_tuple_list = Analyser.get_top_n_words(sorted_word_tuple_list = sorted_essay_word_tuple, n = top_n)
    logging.info("top_n_words_tuple:", top_n_words_tuple_list)
    Analyser.show_top_n_words_dataframe(top_n_words_tuple_list = top_n_words_tuple_list)
    #Analyser.show_top_n_words_plot(top_n_words_tuple_list = top_n_words_tuple_list, n = top_n)
    logging.info("[main]len(essay_word_dict):", len(essay_word_dict))
    '''
    for word in essay_word_dict.keys():
        print word, essay_word_dict[word]
    '''


    # STEP5. (CLASS class_update_in_db.py)
    #        According to word frequency statistic result of essays, insert the statistic result in our essays
    #        (or we can also call them corpus) to field 'showtimes' of data table 'chinese_word_table'.
    database_name = "wordsDB"
    word_table_name = "chinese_word_table"
    Updator.update_showtimes_field(word_dict = essay_word_dict, database_name = word_database_name, table_name = word_table_name)

    logging.info("[main]END at:" + time.strftime('%Y-%m-%d %X', time.localtime()))

################################ PART4 EXECUTE ##################################
if __name__ == "__main__":
    main()