def create_index():
    DOCUMENT = "./document"
    dict = {}
    DATA = "./data"
    pattern = re.compile(r"^[　-ー]$")
    stopwords = {}
    stopwords['という'] = 1
    stopwords['にて'] = 1
    for filename in os.listdir(DOCUMENT):
        print(filename)

        f = codecs.open(DOCUMENT + '/' + filename, 'r', "Shift-JIS", "ignore")
        for line in f:
            tokens = t.tokenize(line)
            for token in tokens:
                if pattern.match(token.surface):
                    continue

                if token.surface in stopwords:
                    continue

                if token.surface in dict:
                    if filename in dict[token.surface]:
                        dict[token.surface][filename] += 1
                    else:
                        dict[token.surface][filename] = 1
                else:
                    dict[token.surface] = {}
                    dict[token.surface][filename] = 1
        f.close()

    return dict

def output(dict):
    INDEX = "./index"
    outfilename = INDEX + "/result.txt"

    f = open(outfilename, 'w')
    for key in sorted(dict):
        for elm in sorted(dict[key]):
            f.write(key + '\t' + elm + '\t' + str(dict[key][elm]))
            f.write("\n")

    f.close()

def calc_idf():
    f_name = "./index/result.txt"
    f2_name = "./index/result2.txt"
    dict = {}
    f = open(f_name)
    f2 = open(f2_name, 'w')

    for line in f:
        line = line.rstrip()
        split_line = line.split("\t")

        word = split_line[0]
        doc = split_line[1]
        freq = int(split_line[2])
        if word in dict:
            dict[word][doc] = freq
        else:
            dict[word] = {}
            dict[word][doc] = freq
        docs = {}
        for word in dict:
            for doc in dict[word]:
                if doc not in docs:
                    docs[doc] = 1
        docs_size = len(docs)
        df = {}
        for key in dict:
            df[key] = len(dict[key])
        idf = {}
        for word in df:
            idf[word] = math.log( ( docs_size / df[word] ) + 1 )
        for word in sorted(dict):
            for doc in sorted(dict[word]):
                tfidf = dict[word][doc] * idf[word]
                f2.write(word + '\t' + doc +'\t' + str(dict[word][doc]) +'\t' + str(idf[word]) + '\t' + str(tfidf) + '\n')

        f.close()
        f2.close()


def do_func():
    dict = create_index()
    output(dict)
    calc_idf()

#---------------------------------------------
# プログラム本体
#---------------------------------------------
import os
from janome.tokenizer import Tokenizer
import codecs
import re
t = Tokenizer()

do_func()
