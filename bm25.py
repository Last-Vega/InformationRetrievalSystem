"""
tf = クエリの出現回数（計算済み）
idf = 計算済み
k1 = 1.2
b = 0.75
k2 = 100
K = k1((1-b)+b*dl/avdl)
dl = 文書長
avdl = 平均文書長
"""

def count_length(DATA):
    length = {}
    pattern = re.compile(r"^[　-ー]$")
    stopwords = {}
    stopwords['という'] = 1
    stopwords['にて'] = 1
    all_sum = 0
    for filename in os.listdir(DATA):
        f = codecs.open(DATA + '/' + filename, 'r', "Shift-JIS", "ignore")
        count = 0
        for line in f:
            tokens = t.tokenize(line)
            for token in tokens:
                if pattern.match(token.surface):
                    continue

                if token.surface in stopwords:
                    continue
            count += len(tokens)
            all_sum += len(tokens)
            length[filename] = count
        f.close()
    length['all'] = all_sum
    return length


def read_file(index_file):
    f = open(index_file, 'r')
    idf_scores = {}
    tf_scores = {}
    for line in f:
        line = line.rstrip()
        split_line = line.split("\t")
        word = split_line[0]
        doc = split_line[1]
        tf = int(split_line[2])
        idf = float(split_line[3])

        idf_scores[word] = idf
        if word in tf_scores:
            tf_scores[word][doc] = tf
        else:
            tf_scores[word] = {}
            tf_scores[word][doc] = tf

    return idf_scores, tf_scores

def deal_with_query(query):
    stopwords = {}
    query_words = {}
    pattern = re.compile(r"^[　-ー]$")
    stopwords['という'] = 1
    stopwords['にて'] = 1
    tokens = t.tokenize(query)
    for token in tokens:
        if pattern.match(token.surface):
            continue
        if token.surface in stopwords:
            continue
        if token.surface in query_words:
            query_words[token.surface] += 1
        else:
            query_words[token.surface] = 1

    return query_words

def identify_docs(query_words, idf_scores, tf_scores):
    ranking_docs = {}
    try:
        for query_word in query_words:
            for doc in tf_scores[query_word]:
                ranking_docs[doc] = 1
    except KeyError:
        print("Please input Japanese sentences.")
        exit()
    return ranking_docs

def calculation(length, idf_scores, tf_scores, ranking_docs, query_words):
    N = 6
    for doc in ranking_docs:
        sum = 0
        k1 = 1.2
        k2 = 100
        b = 0.75
        dl = length[doc]
        avdl = dl/length['all']
        K = k1*((1-b) + b*dl/avdl)
        for query in query_words:
            if doc in tf_scores[query]:
                n = 0
                for k, v in tf_scores[query].items():
                    n += 1
                tf = tf_scores[query][doc]
                idf = math.log((N-n+0.5)/n+0.5)
                numerator = (k1+1)*tf
                denominator = tf + K
                sum += (idf*numerator)/denominator
        """
        try:
            result = math.log(sum)
        except ValueError:
            result = -math.inf
        """
        ranking_docs[doc] = sum
    return ranking_docs

def output(ranking_docs):
    print(sorted(ranking_docs.items(), key=lambda x:x[1], reverse=True))

def do_func():
    length = count_length(DATA)
    idf_scores = read_file(index_file)[0]
    tf_scores = read_file(index_file)[1]
    query_words = deal_with_query(query)
    ranking_docs = identify_docs(query_words, idf_scores, tf_scores)
    ranking_docs = calculation(length, idf_scores, tf_scores, ranking_docs, query_words)
    output(ranking_docs)



#---------------------------------------------
# プログラム本体
#---------------------------------------------
import os
from janome.tokenizer import Tokenizer
import re
import math
import numpy as np
import pandas as pd
import codecs
import time
t = Tokenizer()

#DATA = "./data"
INDEX = "./index"
#index_file = INDEX + "/index2.txt"

DATA = './document'
index_file = INDEX + "/result2.txt"


query = ""
while True:
    input_words = str(input("Query ->"))
    if not input_words:
        break
    else:
        query += "".join(input_words)
print(query)

#query = '吾輩は猫である'
#query = "下人の行方は誰も知らない"

#query = "吾輩"
start = time.time()
do_func()
elapsed_time = time.time() - start
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
