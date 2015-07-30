__author__ = 'yuens'

import MySQLdb
import sys

class import_words_2_db(object):
    def __init__(self):
        pass

    #def __del__(self):
    #    pass

    def create_database(self):
        pass

    def create_table(self):
        pass

    def get_words_from_sogou_method1(self):
        f = open("../data/sogou_cellbase-utf8.txt")
        print type(f)
        print sys.getsizeof(f)
        line = f.readline()
        '''
        while line:
            print line
            print sys.getsizeof(line)

            line = f.readline()
        '''
        f.close()

    def get_words_from_sogou_method2(self):
        f = open("../data/sogou_cellbase-utf8.txt")
        print type(f)
        print sys.getsizeof(f)
        for line in f:
            print line
            print sys.getsizeof(line)


    def get_words_from_sogou_method3(self):
        f = open("../data/sogou_cellbase-utf8.txt")
        lines = f.readlines()
        print sys.getsizeof(lines)


    def import_words_2_db(self):
        pass

test = import_words_2_db()
test.get_words_from_sogou_method1()
#test.get_words_from_sogou_method2()
#test.get_words_from_sogou_method3()