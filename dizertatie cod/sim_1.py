from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

a1 = open('a1.txt', mode="r", encoding="utf8")
a2 = open('a2.txt', mode="r", encoding="utf8")

text_a1 = a1.read()
text_a2 = a2.read()


def get_cosine_sim(*strs):
    vectors = [t for t in get_vectors(*strs)]
    return cosine_similarity(vectors)


def get_vectors(*strs):
    text = [t for t in strs]
    vectorizer = CountVectorizer(text)
    vectorizer.fit(text)
    return vectorizer.transform(text).toarray()


print(get_cosine_sim(text_a1, text_a2))