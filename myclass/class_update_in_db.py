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
        self.start = time.clock()
        logging.basicConfig(level = logging.DEBUG,
                  format = '%(asctime)s  %(filename)19s[line:%(lineno)3d]  %(levelname)5s  %(message)s',
                  datefmt = '%y-%m-%d %H:%M:%S',
                  #filename = 'class_create_databases.log',
                  filename = './main.log',
                  filemode = 'a')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s  %(filename)19s[line:%(lineno)3d]  %(levelname)5s  %(message)s')
        console.setFormatter(formatter)

        logging.getLogger('').addHandler(console)
        logging.info("[update_in_db][__init__]START at " + time.strftime('%Y-%m-%d %X', time.localtime()))
        try:
            self.con = MySQLdb.connect(host = "localhost", user = "root", passwd = "931209", db = database_name, charset = "utf8")
            #print "Connect MySQL database successfully."
            logging.info("[update_in_db][__init__]Connect MySQL database successfully.")
        except MySQLdb.Error, e:
            #print "Connect database failed."
            #print 'MySQL Error %d: %s.' % (e.args[0], e.args[1])
            logging.error("[update_in_db][__init__]Connect database failed.")
            logging.error("[update_in_db][__init__]MySQL Error %d: %s." % (e.args[0], e.args[1]))

    def __del__(self):
        self.con.close()
        self.stop = time.clock()
        #print "Quit MySQL database successfully."
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
        cursor = self.con.cursor()
        word_list = map(lambda word: word.replace("'", '').replace('"', ""), word_dict.keys())
        showtimes_list = map(lambda showtimes: showtimes, word_dict.values())
        try:
            # [VERSION 1]
            map(lambda word, showtimes: cursor.execute("""UPDATE wordsDB.chinese_word_table SET showtimes=showtimes+%s WHERE word='%s'""" % (showtimes, word)), word_list, showtimes_list)
            self.con.commit()
            '''
            # [VERSION 2]
            for idx in xrange(len(word_list)):
                word = word_list[idx]
                showtimes = showtimes_list[idx]
                sql = """UPDATE %s.%s SET showtimes=showtimes+%s WHERE word='%s'""" % (database_name, table_name, showtimes, word)
                cursor.execute(sql)
                self.con.commit()
            '''
        except MySQLdb.Error, e:
            self.con.rollback()
            #print "MySQL Error %d: %s." % (e.args[0], e.args[1])
            logging.error("[update_in_db][update_showtimes_field]MySQL Error %d: %s." % (e.args[0], e.args[1]))



################################### PART3 CLASS TEST ##################################
'''
database_name = "wordsDB"
test = update_in_db(database_name = database_name)
'''