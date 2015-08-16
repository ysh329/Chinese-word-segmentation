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
#import sys
import gc
import os
import re
import time
import logging
################################### PART2 CLASS && FUNCTION ###########################
class import_words_2_db(object):
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
        logging.info("[import_words_2_db][__init__]START at " + time.strftime('%Y-%m-%d %X', time.localtime()))
        try:
            self.con = MySQLdb.connect(host = "localhost", user = "root", passwd = "931209", charset = "utf8")
            logging.info("[import_words_2_db][__init__]Success in connecting MySQL.")
        except MySQLdb.Error, e:
            logging.error("[import_words_2_db][__init__]Fail in connecting MySQL.")
            logging.error("[import_words_2_db][__init__]MySQL Error %d: %s." % (e.args[0], e.args[1]))



    def __del__(self):
        """ Delete a entry of class.
        Args:
            None
        Returns:
            None
        """
        self.con.close()
        self.stop = time.clock()
        logging.info("[import_words_2_db][__del__]Quit database successfully.")
        logging.info("[import_words_2_db][__del__]The class run time is : %.03f seconds" % (self.stop - self.start))
        logging.info("[import_words_2_db][__del__]END at:" + time.strftime('%Y-%m-%d %X', time.localtime()))



    def create_database(self, database_name):
        """ Create database named database_name('wordsDB'), which is used for storing words.
        Args:
            database_name (str): a string stored the database's name prepared to be created.
        Returns:
            None
        """
        try:
            self.con = MySQLdb.connect(host = "localhost", user = "root", passwd = "931209", charset = "utf8")
            logging.info("[import_words_2_db][create_database]Success in connecting MySQL.")
        except MySQLdb.Error, e:
            logging.error("[import_words_2_db][create_database]Fail in connecting MySQL.")
            logging.error("[import_words_2_db][create_database]MySQL Error %d: %s." % (e.args[0], e.args[1]))

        cursor = self.con.cursor()
        sqls = ['SET NAMES UTF8', 'SELECT VERSION()', 'CREATE DATABASE %s' % database_name]
        try:
            map(lambda x: cursor.execute(x), sqls)
            self.con.commit()
            logging.info("[import_words_2_db][create_database]Successfully create database %s in MySQL." % database_name)
        except MySQLdb.Error, e:
            self.con.rollback()
            logging.error('[import_words_2_db][create_database]Fail in executing sqls:%s.' % sqls)
            logging.error('[import_words_2_db][create_database]MySQL Error %d: %s.' % (e.args[0], e.args[1]))



    def create_table(self, database_name, table_name):
        """ Create table(table_name) of database(database_name), which is used for storing words.
        Args:
            database_name   (str): a string stored the database's name..
            table_name      (str): a string stored the table's name prepared to be created.
        Returns:
            None
        """
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
                                corpus_scale INT(11),
                                cixing VARCHAR(10) NOT NULL,
                                type1 VARCHAR(30) NOT NULL,
                                type2 VARCHAR(30) NOT NULL,
                                source VARCHAR(50) NOT NULL,
                                gram INT(11),
                                meaning TEXT NOT NULL,
                                UNIQUE (word)
                                )""" % table_name)
        sqls.append("CREATE INDEX id_idx ON %s(id)" % table_name)
        try:
            map(lambda sql:cursor.execute(sql), sqls)
            self.con.commit()
            logging.info("[import_words_2_db][create_table]Successfully create table %s in MySQL." % table_name)
        except MySQLdb.Error, e:
            self.con.rollback()
            logging.error('[import_words_2_db][create_table]Fail in creating %s table.' % table_name)
            logging.error('[import_words_2_db][create_table]MySQL Error %d: %s.' % (e.args[0], e.args[1]))



    def word_filter(self, word):
        """ As a second filter after attaining from text file, getting the pure word data.
        This process mainly concentrates on recognizing the special symbols and remove them.
        Args:
            word  (str): Chinese word from the modern Chinese dictionary's first filter.
        Returns:
            word  (str): Getting the new word by filtering,
        """
        # filter #1 remove special sign in word
        sign_list=['"', "'", '~','`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=']
        sign_list.extend(["{", "[", "]", "}", "\\", "|", ";", ":", "<", ">", ",", ".", "/", "?"])
        sign_list.extend(['。', '，', '？', '！'])
        for idx in xrange(len(sign_list)):
            sign = sign_list[idx]
            word = word.replace(sign, '')
        # filter #2 remove full width letter
        full_width_letter_list = ['Ａ', 'Ｂ', 'Ｃ', 'Ｄ', 'Ｅ', 'Ｆ', 'Ｇ', 'Ｈ', 'Ｉ', 'Ｊ', 'Ｋ', 'Ｌ', \
                                  'Ｍ', 'Ｎ', 'Ｏ', 'Ｐ', 'Ｑ', 'Ｒ', 'Ｓ', 'Ｔ', 'Ｕ', 'Ｖ', 'Ｗ', 'Ｘ', 'Ｙ', 'Ｚ', \
                                  'ａ', 'ｂ', 'ｃ', 'ｄ', 'ｅ', 'ｆ', 'ｇ', 'ｈ', 'ｉ', 'ｊ', 'ｋ', 'ｌ', 'ｍ', 'ｎ', \
                                  'ｏ', 'ｐ', 'ｑ', 'ｒ', 'ｓ', 'ｔ', 'ｕ', 'ｖ', 'ｗ', 'ｘ', 'ｙ', 'ｚ']
        for idx in xrange(len(full_width_letter_list)):
            letter = full_width_letter_list[idx]
            if word.find(letter) != -1:
                word = word.split(letter)[0]
        # filter #3 judge if exist full width @ symbol. if exists, which means 'word' value is not pure.
        exist_at = word.find('＠')
        if exist_at > -1:
            word = word.split('＠')[0]

        return word



    def insert_modern_chinese_dictionary_2_db(self, file_name, database_name, table_name):
        """ Import words from modern Chinese dictionary to table(table_name) of database(database_name).
        Attain of words from dictionary text file adopts regular expression method.
        Args:
            file_name       (str): Modern Chinese dictionary's file name.
            database_name   (str): The name of database, words will import to this database.
            table_name      (str): The name of table of database, words will import to this database's table.
        Returns:
            None
        """
        logging.info("[import_words_2_db][insert_modern_chinese_dictionary_2_db]Start insert words from modern Chinese dictionary to databse at " + time.strftime('%Y-%m-%d %X', time.localtime()))
        logging.info("[import_words_2_db][insert_modern_chinese_dictionary_2_db]File name of modern chinesedictinonary:%s." % file_name)
        file_dir = os.path.join("./data/", file_name)
        logging.info("[import_words_2_db][insert_modern_chinese_dictionary_2_db]File directory of modern chinesedictinonary:%s." % file_dir)

        try:
            f = open(file_dir)
        except:
            logging.error("[import_words_2_db][insert_modern_chinese_dictionary_2_db]Dictionary file %s doesn't exist." % file_name)
            return

        try:
            logging.info("[import_words_2_db][insert_modern_chinese_dictionary_2_db]Get word and meaning list using parallelize method.")
            lines = f.readlines()
            word_list = sum(map(lambda line: re.compile('…(.*)＠').findall(line.replace('"', '|').replace("'", "|").strip()), lines), [])
            word_list = map(lambda word: self.word_filter(word), word_list)
            meaning_list = sum(map(lambda line: re.compile('＠(.*)').findall(line.replace('"', '|').replace("'", "|").strip()), lines), [])
            logging.info("[import_words_2_db][insert_modern_chinese_dictionary_2_db]len(word_list):%s" % len(word_list))
            logging.info("[import_words_2_db][insert_modern_chinese_dictionary_2_db]word_list[0]:%s" % word_list[0])
            logging.info("[import_words_2_db][insert_modern_chinese_dictionary_2_db]len(meaning_list):%s" % len(meaning_list))
            logging.info("[import_words_2_db][insert_modern_chinese_dictionary_2_db]meaning_list[0]:%s" % meaning_list[0])
        except:
            logging.error("[import_words_2_db][insert_modern_chinese_dictionary_2_db]out of memory, failed in using paralleize method.")
            f.close()
            return
        finally:
            f.close()

        source = file_name
        self.success_insert_meaing_counter = 0
        self.success_insert_meaing_dont_exist_word_counter = 0
        map(lambda word, meaning: self.find_word_and_insert_meaning_2_db(word = word, meaning = meaning, source = source, database_name = database_name, table_name = table_name), word_list, meaning_list)

        logging.info("[import_words_2_db][insert_modern_chinese_dictionary_2_db]finish insert words from modern Chinese dictionary to databse at " + time.strftime('%Y-%m-%d %X', time.localtime()))
        logging.info("[import_words_2_db][insert_modern_chinese_dictionary_2_db]summation of words(or meanings):%s" % len(word_list))
        logging.info("[import_words_2_db][insert_modern_chinese_dictionary_2_db]success inserted words' meaning(exist words before) num.:%d." % self.success_insert_meaing_counter)
        logging.info("[import_words_2_db][insert_modern_chinese_dictionary_2_db]success inserted words' meaning(Dont exist words before) num.:%d." % self.success_insert_meaing_dont_exist_word_counter)
        logging.info("[import_words_2_db][insert_modern_chinese_dictionary_2_db]insert success rate(exist words before):%f." % (self.success_insert_meaing_counter / float(len(word_list))))
        logging.info("[import_words_2_db][insert_modern_chinese_dictionary_2_db]total insert success rate:%f." % ((self.success_insert_meaing_counter + self.success_insert_meaing_dont_exist_word_counter) / float(len(word_list))))
        logging.info("[import_words_2_db][insert_modern_chinese_dictionary_2_db]Completed words'meaning insert task.")

        # garbage collector
        del word_list, meaning_list, f, file_dir
        gc.collect()



    def find_word_and_insert_meaning_2_db(self, word, meaning, source, database_name, table_name):
        """ Find the word in table(table may exist some word previously) and meaning(matching with
         word existed or not word in table) in modern Chinese dictionary text file and then insert the
         meaning and word(if not exist in table previously) into table(table_name) of database(database_name).
        Args:
            word            (str): The word existed in table previously.
            meaning         (str): The meaning from the dictionary text file matches the word in table or not
                            (wil insert both word and meaning).
            source          (str): Describe the source of word. In reality, the source of dictionary is the file
                            name of dictionary.
            database_name   (str): The name of database, words will import to this database.
            table_name      (str): The name of table of database, words will import to this database's table.
        Returns:
            None
        """
        cursor = self.con.cursor()
        if self.success_insert_meaing_counter % 100 == 0:
            logging.info("[import_words_2_db][find_word_and_insert_meaning_2_db]self.success_insert_meaing_counter:%s" % self.success_insert_meaing_counter)
        if self.success_insert_meaing_dont_exist_word_counter % 10 == 0 and self.success_insert_meaing_dont_exist_word_counter != 0:
            logging.info("[import_words_2_db][find_word_and_insert_meaning_2_db]self.success_insert_meaing_dont_exist_word_counter:%s" % self.success_insert_meaing_dont_exist_word_counter)
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
            logging.error("[import_words_2_db][find_word_and_insert_meaning_2_db]abnormal status in MySQL word %s." % word)
            logging.error("[import_words_2_db][find_word_and_insert_meaning_2_db]MySQL Error %d: %s." % (e.args[0], e.args[1]))
        return



    def insert_words_from_file_2_db(self, file_dir, database_name, table_name):
        """ Insert general words(source is sogou) from text file(file_dir, file's directory)
         to table(table_name) of database(database_name).
        Args:
            file_dir        (str): The word existed in table previously.
            database_name   (str): The name of database, words will import to this database.
            table_name      (str): The name of table of database, words will import to this
         database's table.
        Returns:
            None
        """
        logging.info("[import_words_2_db][insert_words_from_file_2_db]start insert words from sogou word file to databse at " + time.strftime('%Y-%m-%d %X', time.localtime()))
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
            logging.info("[import_words_2_db][insert_words_from_file_2_db]insert task finished successfully")
        except MySQLdb.Error, e:
            logging.error("[import_words_2_db][insert_words_from_file_2_db]Fail in connecting MySQL.")
            logging.error("[import_words_2_db][insert_words_from_file_2_db]MySQL Error %d: %s." % (e.args[0], e.args[1]))
        #print type(f)
        #print sys.getsizeof(f)
        try:
            logging.info("[import_words_2_db][insert_words_from_file_2_db]Use parallelization method.")
            # method #2 map method of reading files
            f = open(file_dir,"r")
            lines = f.readlines()
            word_list = map(lambda line: self.get_word_in_line(line), lines)
            pinyin_list = map(lambda line: self.get_pinyin_in_line(line), lines)
            logging.info("[import_words_2_db][insert_words_from_file_2_db]len(word_list):%s" % len(word_list))
            logging.info("[import_words_2_db][insert_words_from_file_2_db]len(pinyin_list):%s" % len(pinyin_list))
            f.close()
            source = "sogou"
            map(lambda word, pinyin: cursor.execute("""INSERT INTO %s(word, pinyin, showtimes, weight, meaning, cixing, type1, type2, source) VALUES('%s', '%s', 0, 0.0, 'ex', 'cx', 't1', 't2', '%s')""" % (table_name, word, pinyin, source)), word_list, pinyin_list)
            self.con.commit()
        except:
            logging.error("[import_words_2_db][insert_words_from_file_2_db]MemoryError, can't use parallelization method, switch to general method.")
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
                        logging.info("[import_words_2_db][insert_words_from_file_2_db]#%d successful insert of word #%d." % (success_counter, counter))
                except MySQLdb.Error, e:
                    self.con.rollback()
                    logging.error("[import_words_2_db][insert_words_from_file_2_db]MySQL Error %d: %s." % (e.args[0], e.args[1]))
            self.words_end_time = time.clock()
            logging.info("[import_words_2_db][insert_words_from_file_2_db]insert task of general words finished at " + time.strftime('%Y-%m-%d %X', time.localtime()) + ".")
            logging.info("[import_words_2_db][insert_words_from_file_2_db]elapsed time of general words insert task: %05f seconds." % (self.words_end_time - self.words_start_time))
            logging.info("[import_words_2_db][insert_words_from_file_2_db]summation of words:%d." % counter)
            logging.info("[import_words_2_db][insert_words_from_file_2_db]success inserted words:%d." % success_counter)
            logging.info("[import_words_2_db][insert_words_from_file_2_db]insert success rate:%f." % (success_counter / float(counter)))
            logging.info("[import_words_2_db][insert_words_from_file_2_db]Completed words insert task.")
        # garbage collector
        del sqls, f, lines, word_list, pinyin_list
        gc.collect()



    def get_word_in_line(self, line):
        """ Get the word in this line from text file using regular expression.
        Args:
            line  (str): line from text file.
        Returns:
            word  (str): word in line.
        """
        word = re.compile(' (.*)').findall(line)[0].replace("'", '').strip()
        return word



    def get_pinyin_in_line(self, line):
        """ Get the pinyin in this line from text file using regular expression.
        Args:
            line  (str): line from text file.
        Returns:
            pinyin  (str): pinyin in line.
        """
        pinyin = re.compile('(.*) ').findall(line)[0].replace("'", '-').strip()
        return pinyin



    def insert_stopwords_from_file_2_db(self, file_dir, database_name, table_name):
        """ Get the stopwords from files, import stopwords to table(table_name) of database(database_name).
        Args:
            file_dir        (str): stopwords files directory.
            database_name   (str): database used for storing stopwords.
            table_name      (str): table used for storing stopwords.
        Returns:
            None
        """
        logging.info("[import_words_2_db][insert_stopwords_from_file_2_db]start insert stopwords to database at " + time.strftime('%Y-%m-%d %X', time.localtime()) + ".")
        cur_directory_list = os.listdir(file_dir)
        stopwords_file_list = filter(lambda file_name: file_name.find("stopwords") > -1, cur_directory_list)

        stopwords_file_directory_list = map(lambda file_name:os.path.join(file_dir, file_name), stopwords_file_list)
        source = "stopwords:" + ",".join(sum(map(lambda file_name: re.compile('(.*)_stopword').findall(file_name), cur_directory_list), []))
        logging.info("[import_words_2_db][insert_stopwords_from_file_2_db]source:%s" % source)
        f_stopwords_list = map(lambda file_dir: open(file_dir), stopwords_file_directory_list)
        stopwords_file_list = map(lambda f: f.readlines(), f_stopwords_list)
        stopwords_list = map(lambda stopword: stopword.strip(), set(sum(stopwords_file_list, [])))
        stopwords_list = filter(lambda stopword: stopword != "", stopwords_list)
        logging.info("[import_words_2_db][insert_stopwords_from_file_2_db]len(stopwords_list):%s" % len(stopwords_list))

        self.stopwords_success_counter = 0
        self.stopwords_start_time = time.clock()
        map(lambda stopword: self.insert_stopword_2_db(database_name, table_name, stopword, source), stopwords_list)
        self.stopwords_end_time = time.clock()
        logging.info("[import_words_2_db][insert_stopwords_from_file_2_db]insert task of stopwords finished at " + time.strftime('%Y-%m-%d %X', time.localtime()) + ".")
        logging.info("[import_words_2_db][insert_stopwords_from_file_2_db]elapsed time of stopwords insert task: %05f seconds." % (self.stopwords_end_time - self.stopwords_start_time))
        logging.info("[import_words_2_db][insert_stopwords_from_file_2_db]all insert num.(contain failed records):%s" % len(stopwords_list))
        logging.info("[import_words_2_db][insert_stopwords_from_file_2_db]sucess insert num.:%s" % self.stopwords_success_counter)
        logging.info("[import_words_2_db][insert_stopwords_from_file_2_db]insert success rate:%0.3f" % (self.stopwords_success_counter / float(len(stopwords_list))))

        # garbage collector
        del cur_directory_list, stopwords_file_list, stopwords_file_directory_list, f_stopwords_list, stopwords_list
        gc.collect()



    def insert_stopword_2_db(self, database_name, table_name, stopword, source):
        """ Insert one stopword to table(table_name) of database(database_name).
        Args:
            database_name   (str): database used for storing stopwords.
            table_name      (str): table used for storing stopwords.
            stopword        (str): one stopword from stopword files.
            source          (str): the source of stopword.
        Returns:
            None
        """
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
            logging.info("[import_words_2_db][insert_stopword_2_db]self.stopwords_success_counter:%s" % self.stopwords_success_counter)
        except MySQLdb.Error, e:
            self.con.rollback()
            logging.error("[import_words_2_db][insert_stopword_2_db]MySQL Error %d: %s." % (e.args[0], e.args[1]))



################################### PART3 CLASS TEST ##################################
'''
# ininitial parameterswohe
database_name = "wordsDB"
table_name = "chinese_word_table"
general_words_file_dir = "../data/sogou_cellbase-utf8.txt"
stopwords_base_dir = "../data/"

test = import_words_2_db()

#test.create_database(database_name = database_name)
#test.create_table(database_name= database_name, table_name = table_name)
#test.insert_words_from_file_2_db(file_dir = general_words_file_dir, database_name = database_name, table_name = table_name)
#test.insert_stopwords_from_file_2_db(file_dir = stopwords_base_dir, database_name = database_name, table_name = table_name)

test.insert_modern_chinese_dictionary_2_db(file_name = 'modern_chinese_dictionary.txt', database_name = database_name, table_name = table_name)
'''