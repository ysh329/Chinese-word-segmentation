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

################################### PART2 CLASS && FUNCTION ###########################
class update_in_db(object):
    def __init__(self, database_name):
        try:
            self.con = MySQLdb.connect(host = "localhost", user = "root", passwd = "931209", db = database_name, charset = "utf8")
            print "Connect MySQL database successfully."
        except:
            print "Connect database failed."
            print 'MySQL Error %d: %s.' % (e.args[0], e.args[1])

    def __del__(self):
        self.con.close()
        print "Quit MySQL database successfully."

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
        word_list = map(lambda word: word, word_dict)
        showtimes_list = map(lambda showtimes: showtimes, word_dict)
        try:
            map(lambda word, showtimes: cursor.execute("""UPDATE SET showtimes=%d FROM %s.%s WHERE word='%s'""" % (showtimes, database_name, table_name, word)), word_list, showtimes_list)
            self.con.commit()
        except MySQLdb.Error, e:
            self.con.rollback()
            print 'MySQL Error %d: %s.' % (e.args[0], e.args[1])



################################### PART3 CLASS TEST ##################################
'''
database_name = "wordsDB"
test = update_in_db(database_name = database_name)
'''