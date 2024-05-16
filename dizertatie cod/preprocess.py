import gensim.downloader as api
from nltk.tokenize import sent_tokenize

import nltk
nltk.download('punkt')

from pyemd import emd

word_vectors = api.load("glove-wiki-gigaword-300")  # load pre-trained word-vectors from gensim-data
a1 = open("a1.txt", "r", encoding="utf8")
a2 = open("a2.txt", "r", encoding="utf8")

text_a1 = a1.read()
text_a2 = a2.read()

senteces_a1 = sent_tokenize(text_a1)
senteces_a2 = sent_tokenize(text_a2)

IDENTIC = []
similarity = []
for i in senteces_a1:
    for j in senteces_a2:
        sim = word_vectors.wmdistance(i, j)
        print(sim)
        if sim < 1:
            similarity.append([i, j])
            print([i, j])
        if sim < 0.5:
            IDENTIC.append([i, j])
            print([i, j])
print(similarity)
print(IDENTIC)