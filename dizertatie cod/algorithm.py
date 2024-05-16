from pprint import pprint

import nltk
nltk.download('stopwords')
nltk.download('punkt')

from nltk.corpus import stopwords
import gensim.downloader as api
from pyemd import emd
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import SequenceMatcher


def preprocessing(file1, file2, flag=0):
    file_one = open(file1, "r", encoding="utf8")
    file_two = open(file2, "r", encoding="utf8")

    text_a1 = file_one.read()
    text_a2 = file_two.read()

    # The word_tokenize() function will break our text phrases into #individual words
    tokens_text1 = sent_tokenize(text_a1)
    tokens_text2 = sent_tokenize(text_a2)

    # we'll create a new list which contains punctuation we wish to clean
    punctuations = ['(',')',';',':','[',']',',','-']

    # We initialize the stopwords variable which is a list of words like #"The", "I", "and", etc. that don't hold much
    # value as keywords
    stop_words = stopwords.words('english')

    # We create a list comprehension which only returns a list of words #that are NOT IN stop_words and NOT IN
    # punctuations.
    phrases_text1 = []
    for i in tokens_text1:
        words = word_tokenize(i)
        keywords = [word for word in words if not word in stop_words and not word in punctuations]
        phrases_text1.append(' '.join(keywords))

    phrases_text2 = []
    for i in tokens_text2:
        words = word_tokenize(i)
        keywords = [word for word in words if not word in stop_words and not word in punctuations]
        phrases_text2.append(' '.join(keywords))

    if flag == 1:
        return tokens_text1, tokens_text2
    return phrases_text1, phrases_text2


#----------------------word_vectors------------------
def word_vectors(file1, file2):
    phrases_text1, phrases_text2 = preprocessing(file1, file2, 1)
    pprint(phrases_text1)
    pprint(phrases_text2)
    word_vectors = api.load("glove-wiki-gigaword-300")
    IDENTIC = []
    similarity = []

    for i in phrases_text1:
        for j in phrases_text2:
            sim = word_vectors.wmdistance(i, j)
            if 0.6 < sim < 1:
                similarity.append([i, j, sim])
            if sim < 0.4:
                IDENTIC.append([i, j, sim])
    print('Identic: ')
    pprint(IDENTIC)
    print('Similar: ')
    pprint(similarity)


print('------------' + 'word_vectors' + '--------------')
word_vectors("a1.txt", "a2.txt")
print('---------------------------------------------------')


#----------------------Sequence_Matcher-------------------------------
def Sequence_Matcher(file1, file2):
    phrases_text1, phrases_text2 = preprocessing(file1, file2, 1)
    IDENTIC = []
    similarity = []
    for i in phrases_text1:
        for j in phrases_text2:
            m = SequenceMatcher(None, i, j)

            if 0.6 < m.ratio() < 0.95:
                similarity.append([i, j])
            if m.ratio() > 0.95:
                IDENTIC.append([i, j])
    print('Similar: ')
    pprint(similarity)
    print('\nIdentic: ')
    pprint(IDENTIC)


print('------------' + 'SequenceMatcher' + '--------------')
Sequence_Matcher('a1.txt', "a2.txt")
print('---------------------------------------------------')



#------------------------cosine_sim----------------------------
def get_cosine_sim(*strs):
    vectors = [t for t in get_vectors(*strs)]
    return cosine_similarity(vectors)


def get_vectors(*strs):
    text = [t for t in strs]
    vectorizer = CountVectorizer(text)
    vectorizer.fit(text)
    return vectorizer.transform(text).toarray()


a1 = open('a1.txt', mode="r", encoding="utf8")
a2 = open('a2.txt', mode="r", encoding="utf8")

text_a1 = a1.read()
text_a2 = a2.read()

print('\n------------' + 'cosine_sim' + '--------------')
print(get_cosine_sim(text_a1, text_a2)[0][1], '%')
print('---------------------------------------------------')