import math
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
