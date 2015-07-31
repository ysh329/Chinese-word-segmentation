# -*- coding: utf-8 -*-
# !/usr/bin/python
################################### PART0 DESCRIPTION #################################
# Filename: class_import_words_2_db.py
# Description:
#             import file's words of lines in sogou_cellbase-utf8.txt
#      to database named "chinese_wordsDB"'s table "chinese_words_table",
#      which contains (id, word, pinyin, explan, )

# Author: Shuai Yuan
# E-mail: ysh329@sina.com
# Create: 2015-7-31
# Last:
__author__ = 'yuens'
################################### PART1 IMPORT ######################################
import MySQLdb
import sys
import re
import time
################################### PART2 CLASS && FUNCTION ###########################
class import_words_2_db(object):
    def __init__(self):
        self.start = time.clock()

    def __del__(self):
        self.con.close()
        self.end = time.clock()
        print "The function run time is : %.03f seconds" % (self.end - self.start)

    def dbcommit(self):
        self.con.commit()

    def dbrollback(self):
        self.con.rollback()

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
            self.dbcommit()
        except MySQLdb.Error, e:
            self.dbrollback()
            print 'Fail in creating database %s.' % database_name
            print 'MySQL Error %d: %s.' % (e.args[0], e.args[1])


    def create_table(self, database_name, table_name):
        cursor = self.con.cursor()

        sqls = ['USE %s' % database_name, 'SET NAMES UTF8']
        sqls.append("ALTER DATABASE %s DEFAULT CHARACTER SET 'utf8'" % database_name)
        sqls.append("""CREATE TABLE IF NOT EXISTS %s(
                                id INT(11) AUTO_INCREMENT PRIMARY KEY,
                                word VARCHAR(30) NOT NULL,
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
            map(lambda x: cursor.execute(x), sqls)
            self.dbcommit()
        except MySQLdb.Error, e:
            self.dbrollback()
            print 'Fail in creating %s table.' % table_name
            print 'MySQL Error %d: %s.' % (e.args[0], e.args[1])


    def get_words_from_sogou(self, file_dir, database_name, table_name):
        f = open(file_dir)
        cursor = self.con.cursor()
        sqls = ["ALTER DATABASE %s DEFAULT CHARACTER SET 'utf8'" % database_name]
        sqls.append("set character_set_database=utf8")
        sqls.append("set character_set_filesystem=utf8")
        sqls.append("set character_set_server=utf8")
        sqls.append("SET NAMES UTF8")
        try:
            map(lambda sql: cursor.execute(sql), sqls)
            self.dbcommit()
        except MySQLdb.Error, e:
            print 'Fail in connecting MySQL.'
            print 'MySQL Error %d: %s.' % (e.args[0], e.args[1])

        #print type(f)
        #print sys.getsizeof(f)

        counter = 0
        success_counter = 0
        for line in f:
            counter += 1

            word = re.compile(' (.*)').findall(line)[0].strip()
            pinyin = re.compile('(.*) ').findall(line)[0].replace("'", '-').strip()
            source = "sougou"
            try:
                sqls = []
                #cursor.execute("""INSERT INTO %s(word, pinyin, showtimes, weight, explan, type1, type2, cixing, source)
                #        VALUES ('%s', '%s', 0, 0.0, '', '', '', '', '%s')""" % (table_name, word, pinyin, source))
                sqls.append("""INSERT INTO %s(word, pinyin, showtimes, weight, meaning, cixing, type1, type2, source) VALUES('%s', '%s', 0, 0.0, 'ex', 'cx', 't1', 't2', '%s')""" % (table_name, word, pinyin, source))
                map(lambda sql: cursor.execute(sql), sqls)
                self.dbcommit()
                success_counter += 1
                if success_counter % 10000 == 0:
                    print "#%d successful insert of word #%d." % (success_counter, counter)
            except MySQLdb.Error, e:
                self.dbrollback()
                print 'MySQL Error %d: %s.' % (e.args[0], e.args[1])

        f.close()
        print "summation of words:%d." % counter
        print "success inserted words:%d." % success_counter
        print "insert success rate:%f." % (success_counter / float(counter))


test = import_words_2_db()
test.create_database(database_name = "chinese_wordsDB")
test.create_table(database_name= "chinese_wordsDB", table_name = "chinese_word_table")
test.get_words_from_sogou(file_dir = "../data/sogou_cellbase-utf8.txt", database_name = "chinese_wordsDB", table_name = "chinese_word_table")