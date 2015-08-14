# -*- coding: utf-8 -*-
# !/usr/bin/python
################################### PART0 DESCRIPTION #################################
# Filename: class_update_in_db.py
# Description:
#             Update some fields in table of database, such as judge if the word is a
#       chinese char or english words(based on letter) or a symbol, etc.
#             This process is like a ETL's pre-process more or less. Besides operation below, it also
#       contains check and delete the repeated records and abnormal records.
#             Table structure:(id, word, pinyin, showtimes, weight, meaning, cixing, type1, type2, source)

# Author: Shuai Yuan
# E-mail: ysh329@sina.com
# Create: 2015-8-4 08:48:57
# Last:
__author__ = 'yuens'
################################### PART1 IMPORT ######################################
import MySQLdb
import logging
import time
################################### PART2 CLASS && FUNCTION ###########################
class update_in_db(object):
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
        logging.info("[update_in_db][__init__]START at " + time.strftime('%Y-%m-%d %X', time.localtime()))
        try:
            self.con = MySQLdb.connect(host = "localhost", user = "root", passwd = "931209", db = database_name, charset = "utf8")
            logging.info("[update_in_db][__init__]Connect MySQL database successfully.")
        except MySQLdb.Error, e:
            logging.error("[update_in_db][__init__]Connect database failed.")
            logging.error("[update_in_db][__init__]MySQL Error %d: %s." % (e.args[0], e.args[1]))

    def __del__(self):
        """ Delete a entry of class.
        Args:
            None
        Returns:
            None
        """
        self.con.close()
        self.stop = time.clock()
        logging.info("[update_in_db][__del__]Quit MySQL database successfully.")
        logging.info("[update_in_db][__del__]The class run time is : %.03f seconds" % (self.stop - self.start))
        logging.info("[update_in_db][__del__]END at:" + time.strftime('%Y-%m-%d %X', time.localtime()))

    def remove_repeated_reocrd(self):
        """according to the value of field word"""
        pass

    def update_id_field(self):
        pass

    def update_pinyin_field(self):
        '''recognize chinese character or english word'''
        pass

    def update_source_field(self):
        pass

    def update_meaning_field(self):
        pass

    def update_cixing_field(self):
        pass

    def update_showtimes_field(self, word_dict, database_name, table_name):
        """ Update the showtimes field in table(table_name) of database(database_name)
         according to the result of words frequency statistic(word_dict).
        Args:
            word_dict       (dict): A dictionary contains all unique words in essay_word_2d_list,
         which is a key-value form(key: word, value: word frequency).
            database_name   (str): The name of database which will be updated.
            table_name      (str): The name of table of database which will be updated.
        Returns:
            None
        """
        cursor = self.con.cursor()
        word_list = map(lambda word: word.replace("'", '').replace('"', ""), word_dict.keys())
        showtimes_list = map(lambda showtimes: showtimes, word_dict.values())
        try:
            map(lambda word, showtimes: cursor.execute("""UPDATE wordsDB.chinese_word_table SET showtimes=showtimes+%s WHERE word='%s'""" % (showtimes, word)), word_list, showtimes_list)
            self.con.commit()
            logging.info("[update_in_db][update_showtimes_field]Update words' showtimes failed.")
        except MySQLdb.Error, e:
            self.con.rollback()
            logging.error("[update_in_db][update_showtimes_field]Update words' showtimes failed.")
            logging.error("[update_in_db][update_showtimes_field]MySQL Error %d: %s." % (e.args[0], e.args[1]))



################################### PART3 CLASS TEST ##################################
'''
database_name = "wordsDB"
test = update_in_db(database_name = database_name)
'''