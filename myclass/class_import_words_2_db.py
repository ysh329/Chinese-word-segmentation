# -*- coding: utf-8 -*-
# !/usr/bin/python
################################### PART0 DESCRIPTION #################################
# Filename: class_import_words_2_db.py
# Description:
#             import file's words of lines in sogou_cellbase-utf8.txt
#      to database named "chinese_wordsDB"'s table "chinese_words_table",
#      which contains 10 fields(id, word, pinyin, showtimes, weight, meaning, cixing, type1, type2, source).

# Author: Shuai Yuan
# E-mail: ysh329@sina.com
# Create: 2015-7-31
# Last:
__author__ = 'yuens'
################################### PART1 IMPORT ######################################
import MySQLdb
import sys
import gc
import os
import re
import time
################################### PART2 CLASS && FUNCTION ###########################
class import_words_2_db(object):
    def __init__(self):
        print "start at:" + time.strftime('%Y-%m-%d %X', time.localtime())
        self.start = time.clock()
        self.con = MySQLdb.connect(host = "localhost", user = "root", passwd = "931209", charset = "utf8")

    def __del__(self):
        self.con.close()
        self.stop = time.clock()
        print "The function run time is : %.03f seconds" % (self.stop - self.start)
        print "end at:" + time.strftime('%Y-%m-%d %X', time.localtime())



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
        sqls.append("""CREATE TABLE IF NOT EXISTS %s
                                (
                                id INT(11) AUTO_INCREMENT PRIMARY KEY,
                                word VARCHAR(100) NOT NULL,
                                pinyin VARCHAR(100) NOT NULL,
                                showtimes INT(11) NOT NULL DEFAULT 0,
                                weight FLOAT(11) NOT NULL DEFAULT 0.0,
                                cixing VARCHAR(10) NOT NULL,
                                type1 VARCHAR(30) NOT NULL,
                                type2 VARCHAR(30) NOT NULL,
                                source VARCHAR(50) NOT NULL,
                                meaning TEXT NOT NULL,
                                UNIQUE (word)
                                )""" % table_name)
        sqls.append("CREATE INDEX id_idx ON %s(id)" % table_name)
        #print sqls
        try:
            map(lambda sql:cursor.execute(sql), sqls)
            self.con.commit()
        except MySQLdb.Error, e:
            self.con.rollback()
            print 'Fail in creating %s table.' % table_name
            print 'MySQL Error %d: %s.' % (e.args[0], e.args[1])


    def insert_modern_chinese_dictionary_2_db(self, file_name, database_name, table_name):
        print "start insert words from modern Chinese dictionary to databse at " + time.strftime('%Y-%m-%d %X', time.localtime())
        print "file_name:", file_name
        file_dir = os.path.join("../data/", file_name)
        print "file_dir:", file_dir
        try: f = open(file_dir)
        except: print "file %s doesn't exist." % file_name; return

        try:
            print "use parallelize method."
            lines = f.readlines()
            word_list = sum(map(lambda line: re.compile('…(.*)＠').findall(line.replace('"', '|').replace("'", "|").strip()), lines), [])
            meaning_list = sum(map(lambda line: re.compile('＠(.*)').findall(line.replace('"', '|').replace("'", "|").strip()), lines), [])
            print "len(word_list):", len(word_list)
            print "word_list[0]:", word_list[0]
            print "len(meaning_list):", len(meaning_list)
            print "meaning_list[0]:", meaning_list[0]
        except:
            print "out of memory, failed in using paralleize method."
            f.close()
            return
        finally:
            f.close()

        source = file_name
        self.success_insert_meaing_counter = 0
        self.success_insert_meaing_dont_exist_word_counter = 0
        map(lambda word, meaning: self.find_word_and_insert_meaning_2_db(word = word, meaning = meaning, source = source, database_name = database_name, table_name = table_name), word_list, meaning_list)

        print "finish insert words from modern Chinese dictionary to databse at " + time.strftime('%Y-%m-%d %X', time.localtime())
        print "summation of words(or meanings):%d." % len(word_list)
        print "success inserted words' meaning(exist words before) num.:%d." % self.success_insert_meaing_counter
        print "success inserted words' meaning(Dont exist words before) num.:%d." % self.success_insert_meaing_dont_exist_word_counter
        print "insert success rate(exist words before):%f." % (self.success_insert_meaing_counter / float(len(word_list)))
        print "total insert success rate:%f." % ((self.success_insert_meaing_counter + self.success_insert_meaing_dont_exist_word_counter) / float(len(word_list)))
        print "Completed words'meaning insert task."

        # garbage collector
        del word_list, meaning_list, f, file_dir
        gc.collect()


    def find_word_and_insert_meaning_2_db(self, word, meaning, source, database_name, table_name):
        cursor = self.con.cursor()
        if self.success_insert_meaing_counter % 100 == 0: print "self.success_insert_meaing_counter:", self.success_insert_meaing_counter
        if self.success_insert_meaing_dont_exist_word_counter % 10 == 0 and self.success_insert_meaing_dont_exist_word_counter != 0:
            print "self.success_insert_meaing_dont_exist_word_counter:", self.success_insert_meaing_dont_exist_word_counter
        try:
            cursor.execute("SELECT id FROM %s.%s WHERE word='%s'" % (database_name, table_name, word))
            word_id = cursor.fetchone()
            if word_id != None:
                word_id = int(word_id[0])
                cursor.execute("""UPDATE %s.%s set meaning="%s", source="%s" WHERE id=%s """ % (database_name, table_name, meaning, source, word_id))

                self.success_insert_meaing_counter += 1
            else: # word_id == None
                sql = """INSERT INTO %s.%s
                        (word, pinyin, showtimes, weight, meaning, cixing, type1, type2, source)
                        VALUES('%s', '', 0, 0.0, '%s', 'cx', 't1', 't2', '%s')""" % (database_name, table_name, word, meaning, source)
                cursor.execute(sql)
                self.success_insert_meaing_dont_exist_word_counter += 1
            self.con.commit()
        except MySQLdb.Error, e:
            print "abnormal status in MySQL word %s." % word
            print 'MySQL Error %d: %s.' % (e.args[0], e.args[1])
        return


    def insert_words_from_file_2_db(self, file_dir, database_name, table_name):
        print "start insert words from sogou word file to databse at " + time.strftime('%Y-%m-%d %X', time.localtime())
        self.words_start_time = time.clock()

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
            self.words_end_time = time.clock()
            print "insert task of general words finished at " + time.strftime('%Y-%m-%d %X', time.localtime()) + "."
            print "elapsed time of general words insert task: %05f seconds." % (self.words_end_time - self.words_start_time)
            print "summation of words:%d." % counter
            print "success inserted words:%d." % success_counter
            print "insert success rate:%f." % (success_counter / float(counter))
            print "Completed words insert task."

        # garbage collector
        del sqls, f, lines, word_list, pinyin_list, counter, success_counter, word, pinyin, sql
        gc.collect()

    def get_word_in_line(self, line):
        word = re.compile(' (.*)').findall(line)[0].replace("'", '').strip()
        return word



    def get_pinyin_in_line(self, line):
        pinyin = re.compile('(.*) ').findall(line)[0].replace("'", '-').strip()
        return pinyin



    def insert_stopwords_from_file_2_db(self, file_dir, database_name, table_name):
        print "start insert stopwords to database at " + time.strftime('%Y-%m-%d %X', time.localtime()) + "."
        cur_directory_list = os.listdir(file_dir)
        stopwords_file_list = filter(lambda file_name: file_name.find("stopwords") > -1, cur_directory_list)

        stopwords_file_directory_list = map(lambda file_name:os.path.join(file_dir, file_name), stopwords_file_list)
        source = "stopwords:" + ",".join(sum(map(lambda file_name: re.compile('(.*)_stopword').findall(file_name), cur_directory_list), []))
        print "source:", source
        #try:
        f_stopwords_list = map(lambda file_dir: open(file_dir), stopwords_file_directory_list)
        stopwords_file_list = map(lambda f: f.readlines(), f_stopwords_list)
        stopwords_list = map(lambda stopword: stopword.strip(), set(sum(stopwords_file_list, [])))
        stopwords_list = filter(lambda stopword: stopword != "", stopwords_list)
        print "len(stopwords_list):", len(stopwords_list)

        self.stopwords_success_counter = 0
        self.stopwords_start_time = time.clock()
        # [method #1]
        '''
        for idx in xrange(len(stopwords_list)):
            stopword = stopwords_list[idx]
            self.insert_stopword_2_db(database_name = database_name,\
                                      table_name = table_name,\
                                      stopword = stopword,\
                                      source = source)
        '''
        # [method #2]
        map(lambda stopword: self.insert_stopword_2_db(database_name, table_name, stopword, source), stopwords_list)
        # insert word " abd \
        '''
        try:
            cursor = self.con.cursor()
            cursor.execute('insert wordsDB.chinese_word_table(word, pinyin, showtimes, weight, meaning, cixing, type1, type2, source) VALUES("\\", "", 0, 0.0, "ex", "cx", "stopword", "t2", "stopwords:hit,chinese,scu,sc_ot,baidu")')
            self.con.commit()
            self.stopwords_success_counter += 1
            cursor.execute("insert wordsDB.chinese_word_table(word, pinyin, showtimes, weight, meaning, cixing, type1, type2, source) VALUES('\"', '', 0, 0.0, 'ex', 'cx', 'stopword', 't2', 'stopwords:hit,chinese,scu,sc_ot,baidu')")
            self.con.commit()
            self.stopwords_success_counter += 1
            print "insert words('\\' and '\"') successfully."
        except MySQLdb.Error, e:
            self.con.rollback()
            print 'MySQL Error %d: %s.' % (e.args[0], e.args[1])
        '''

        self.stopwords_end_time = time.clock()
        print "insert task of stopwords finished at " + time.strftime('%Y-%m-%d %X', time.localtime()) + "."
        print "elapsed time of stopwords insert task: %05f seconds." % (self.stopwords_end_time - self.stopwords_start_time)
        print "all insert num.(contain failed records):", len(stopwords_list)
        print "sucess insert num.:", self.stopwords_success_counter
        print "insert success rate:%0.3f" % (self.stopwords_success_counter / float(len(stopwords_list)))

        # garbage collector
        del cur_directory_list, stopwords_file_list, stopwords_file_directory_list, f_stopwords_list, stopwords_base_dir, stopwords_list
        gc.collect()


    def insert_stopword_2_db(self, database_name, table_name, stopword, source):
        cursor = self.con.cursor()
        try:
            cursor.execute("""SELECT id FROM %s.%s WHERE word="%s" """ % (database_name, table_name, stopword))
            word_exist = cursor.fetchone() > 0
            if word_exist:
                if source != '\\' or source != '"':
                    sql = """UPDATE %s.%s
                 SET type1='stopword',
                  source='%s'
                   WHERE word="%s" """ % (database_name, table_name, source, stopword)
                cursor.execute(sql)
                self.con.commit()
            else:
                if source != '\\' or source != '"':
                    sql = """INSERT INTO %s.%s
                (word, pinyin, showtimes, weight, meaning, cixing, type1, type2, source)
                VALUES("%s", '', 0, 0.0, 'ex', 'cx', 'stopword', 't2', '%s')""" % (database_name, table_name, stopword, source)
                cursor.execute(sql)
                self.con.commit()
            self.stopwords_success_counter += 1
            print "self.stopwords_success_counter:", self.stopwords_success_counter
        except MySQLdb.Error, e:
            self.con.rollback()
            print 'MySQL Error %d: %s.' % (e.args[0], e.args[1])



################################### PART3 CLASS TEST ##################################
# initial parameterswohe
database_name = "wordsDB"
table_name = "chinese_word_table"
general_words_file_dir = "../data/sogou_cellbase-utf8.txt"
stopwords_base_dir = "../data/"

test = import_words_2_db()
'''
test.create_database(database_name = database_name)
test.create_table(database_name= database_name, table_name = table_name)
test.insert_words_from_file_2_db(file_dir = general_words_file_dir, database_name = database_name, table_name = table_name)
test.insert_stopwords_from_file_2_db(file_dir = stopwords_base_dir, database_name = database_name, table_name = table_name)
'''
test.insert_modern_chinese_dictionary_2_db(file_name = 'modern_chinese_dictionary.txt', database_name = database_name, table_name = table_name)
