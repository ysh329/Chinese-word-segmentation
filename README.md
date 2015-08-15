Chinese-word-segmentation
=======
Accomplish Chinese word segmentation by Python.

## Part 0.Description

## Part 1.Class Description
1. STEP1. (CLASS class_import_words_2_db.py)  
Import words data from Sogou's cell words base and Chinese modern dictionary
to database 'wordsDB' table 'chinese_word_table'.
2. STEP2. (CLASS class_update_in_db.py)  
Update or increase table's some fields, such as 'pinyin', 'meaning' fields, etc.
3. STEP3. (CLASS class_bidirectional_matching_algorithm.py)  
Make Chinese word segmentation by MM and RMM methods.
4. STEP4. (CLASS class_segmentation_result_analyser.py)  
Analise the result of Chinese word segmentation step, such as word frequency
statistic, result visualization, etc.
5. STEP5. (CLASS class_update_in_db.py)  
According to word frequency statistic result of essays, insert the statistic result in our essays
(or we can also call them corpus) to field 'showtimes' of data table 'chinese_word_table'.

## Part 2.Unsolved problems
- Can't insert stopwords(" and \ ) to database, but it works in MYSQL.  
 So if you want to insert symbols " and \, you can insert them in MySQL directly.