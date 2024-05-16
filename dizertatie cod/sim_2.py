from difflib import SequenceMatcher

from nltk.tokenize import sent_tokenize

a1 = open('a1.txt', mode="r", encoding="utf8")
a2 = open('a2.txt', mode="r", encoding="utf8")

text_a1 = a1.read()
text_a2 = a2.read()
senteces_a1 = sent_tokenize(text_a1)
senteces_a2 = sent_tokenize(text_a2)
IDENTIC = []
similarity = []
for i in senteces_a1:
    for j in senteces_a2:
        m = SequenceMatcher(None, i, j)
        similarity.append(m.ratio())
        if m.ratio() > 0.6:
            print(i)
            print(j)

print(similarity)