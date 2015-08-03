# -*- coding: utf-8 -*-
# !/usr/bin/python
################################### PART0 DESCRIPTION #################################
# Filename: class_import_words_2_db.py
# Description:
#             import file's words of lines in sogou_cellbase-utf8.txt
#      to database named "chinese_wordsDB"'s table "chinese_words_table",
#      which contains (id, word, pinyin, meaning, )

# Author: Shuai Yuan
# E-mail: ysh329@sina.com
# Create: 2015-7-31
# Last:
__author__ = 'yuens'
################################### PART1 IMPORT ######################################
import MySQLdb
import sys
import os
import re
from time import clock
################################### PART2 CLASS && FUNCTION ###########################
class import_words_2_db(object):
    def __init__(self):
        self.start = clock()



    def __del__(self):
        self.con.close()
        print "The function run time is : %.03f seconds" % (clock() - self.start)



    def create_database(self, database_name):
        try:
            self.con = MySQLdb.connect(host = "localhost", user = "root", passwd = "931209", charset = "utf8")
        except MySQLdb.Error, e:
            print 'Fail in connecting MySQL.'
            print 'MySQL Error %d: %s.' % (e.args[0], e.args[1])

        cursor = self.con.cursor()
        sqls = ['SET NAMES UTF8', 'SELECT VERSION()', 'CREATE DATABASE %s' % database_name]
        try:
            map(lambda x: cursor.execute(x), sqls)
            self.con.commit()
        except MySQLdb.Error, e:
            self.con.rollback()
            print 'Fail in creating database %s.' % database_name
            print 'MySQL Error %d: %s.' % (e.args[0], e.args[1])



    def create_table(self, database_name, table_name):
        cursor = self.con.cursor()

        sqls = ['USE %s' % database_name, 'SET NAMES UTF8']
        sqls.append("ALTER DATABASE %s DEFAULT CHARACTER SET 'utf8'" % database_name)
        sqls.append("""CREATE TABLE IF NOT EXISTS %s(
                                id INT(11) AUTO_INCREMENT PRIMARY KEY,
                                word TEXT NOT NULL,
                                pinyin TEXT NOT NULL,
                                showtimes INT(11) NOT NULL DEFAULT 0,
                                weight FLOAT(11) NOT NULL DEFAULT 0.0,
                                meaning TEXT NOT NULL,
                                cixing VARCHAR(10) NOT NULL,
                                type1 VARCHAR(30) NOT NULL,
                                type2 VARCHAR(30) NOT NULL,
                                source TEXT NOT NULL)""" % table_name)
        sqls.append("CREATE INDEX id_idx ON %s(id)" % table_name)
        #print sqls
        try:
            map(lambda sql:cursor.execute(sql), sqls)
            self.con.commit()
        except MySQLdb.Error, e:
            self.con.rollback()
            print 'Fail in creating %s table.' % table_name
            print 'MySQL Error %d: %s.' % (e.args[0], e.args[1])



    def insert_words_from_file_2_db(self, file_dir, database_name, table_name):

        cursor = self.con.cursor()
        sqls = ["ALTER DATABASE %s DEFAULT CHARACTER SET 'UTF8'" % database_name]
        sqls.append("SET NAMES UTF8")
        '''
        sqls.append("SET CHARACTER_SET_DATABASE=UTF8")
        sqls.append("SET CHARACTER_SET_FILESYSTEM=UTF8")
        sqls.append("SET CHARACTER_SET_SERVER=UTF8")
        '''
        try:
            map(lambda sql: cursor.execute(sql), sqls)
            self.con.commit()
        except MySQLdb.Error, e:
            print 'Fail in connecting MySQL.'
            print 'MySQL Error %d: %s.' % (e.args[0], e.args[1])

        #print type(f)
        #print sys.getsizeof(f)

        try:
            print "Use parallelization method."
            # method #2 map method of reading files
            f = open(file_dir,"r")
            lines = f.readlines()
            word_list = map(lambda line: self.get_word_in_line(line), lines)
            pinyin_list = map(lambda line: self.get_pinyin_in_line(line), lines)
            print "len(word_list):", len(word_list)
            print "len(pinyin_list):", len(pinyin_list)
            f.close()

            source = "sogou"
            map(lambda word, pinyin: cursor.execute("""INSERT INTO %s(word, pinyin, showtimes, weight, meaning, cixing, type1, type2, source) VALUES('%s', '%s', 0, 0.0, 'ex', 'cx', 't1', 't2', '%s')""" % (table_name, word, pinyin, source)), word_list, pinyin_list)
            self.con.commit()
        except:
            print "MemoryError, can't use parallelization method, switch to general method."
            # method #1 for-loop method of reading files
            counter = 0
            success_counter = 0
            f = open(file_dir)
            for line in f:
                counter += 1
                word = re.compile(' (.*)').findall(line)[0].replace("'", '').strip()
                pinyin = re.compile('(.*) ').findall(line)[0].replace("'", '-').strip()
                source = "sogou"
                try:
                    sql = """INSERT INTO %s(word, pinyin, showtimes, weight, meaning, cixing, type1, type2, source) VALUES('%s', '%s', 0, 0.0, 'ex', 'cx', 't1', 't2', '%s')""" % (table_name, word, pinyin, source)
                    cursor.execute(sql)
                    self.con.commit()
                    success_counter += 1
                    if success_counter % 1000 == 0:
                        print "#%d successful insert of word #%d." % (success_counter, counter)
                except MySQLdb.Error, e:
                    self.con.rollback()
                    print 'MySQL Error %d: %s.' % (e.args[0], e.args[1])

            print "summation of words:%d." % counter
            print "success inserted words:%d." % success_counter
            print "insert success rate:%f." % (success_counter / float(counter))
        print "Completed words insert task."



    def get_word_in_line(self, line):
        word = re.compile(' (.*)').findall(line)[0].replace("'", '').strip()
        return word



    def get_pinyin_in_line(self, line):
        pinyin = re.compile('(.*) ').findall(line)[0].replace("'", '-').strip()
        return pinyin



    def insert_stopwords_from_file_2_db(self, file_dir, database_name, table_name):
        print "prepare insert stopwords to database."
        cur_directory_list = os.listdir(file_dir)
        stopwords_file_list = filter(lambda file_name: file_name.find("stopwords") > -1, cur_directory_list)

        stopwords_file_directory_list = map(lambda file_name:os.path.join(file_dir, file_name), stopwords_file_list)
        source = "stopwords:" + ",".join(sum(map(lambda file_name: re.compile('(.*)_stopword').findall(file_name), cur_directory_list), []))
        print "source:", source
        #try:
        f_stopwords_list = map(lambda file_dir: open(file_dir), stopwords_file_directory_list)
        stopwords_file_list = map(lambda f: f.readlines(), f_stopwords_list)
        stopwords_list = map(lambda stopword: stopword.strip(), set(sum(stopwords_file_list, [])))
        print "len(stopwords_list):", len(stopwords_list)


        # [method #1]
        for idx in xrange(len(stopwords_list)):
            stopword = stopwords_list[idx]
            self.insert_stopword_2_db(database_name = database_name,\
                                      table_name = table_name,\
                                      stopword = stopword,\
                                      source = source)
            # [method #2]
            #map(lambda stopword: self.insert_stopword_2_db(database_name, table_name, stopword, source), stopwords_list)
        '''
        except:
            print "Out of memory."
            return
        '''
        print "insert task of stopwords finished."


    def insert_stopword_2_db(self, database_name, table_name, stopword, source):
#        self.con = MySQLdb.connect(host = "localhost", user = "root", passwd = "931209", db = table_name, charset = "utf8")
        cursor = self.con.cursor()
        try:
            cursor.execute("""SELECT id FROM %s.%s WHERE word='%s'""" % (database_name, table_name, stopword))
            word_exist = cursor.fetchone() > 0
            if word_exist:
                cursor.execute("""UPDATE %s.%s SET type1='stopword', source='%s' WHERE word='%s'""" % (database_name, table_name, source, stopword))
                self.con.commit()
            else:
                cursor.execute("""INSERT INTO %s.%s(word, pinyin, showtimes, weight, meaning, cixing, type1, type2, source) VALUES('%s', '', 0, 0.0, 'ex', 'cx', 'stopword', 'tx', '%s')""" % (database_name, table_name, stopword, source))
                self.con.commit()
        except MySQLdb.Error, e:
            self.con.rollback()
            print 'MySQL Error %d: %s.' % (e.args[0], e.args[1])



################################### PART3 CLASS TEST ##################################
# initial parameters
database_name = "wordsDB"
table_name = "chinese_word_table"
general_words_file_dir = "../data/sogou_cellbase-utf8.txt"
stopwords_base_dir = "../data/"

test = import_words_2_db()

test.create_database(database_name = database_name)
test.create_table(database_name= database_name, table_name = table_name)
'''
test.insert_words_from_file_2_db(file_dir = general_words_file_dir, database_name = database_name, table_name = table_name)
'''
test.insert_stopwords_from_file_2_db(file_dir = stopwords_base_dir, database_name = database_name, table_name = table_name)
