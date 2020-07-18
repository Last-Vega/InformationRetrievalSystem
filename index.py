def create_index():
    DATA = "./data"
    dict = {}

    pattern = re.compile(r"^[　-ー]$")
    stopwords = {}
    stopwords['という'] = 1
    stopwords['にて'] = 1

    for filename in os.listdir(DATA):
        f = open(DATA + '/' + filename, 'r')

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


#---------------------------------------------
# プログラム本体
#---------------------------------------------
import os
from janome.tokenizer import Tokenizer
import re
t = Tokenizer()

create_index()
