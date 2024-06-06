from sklearn.feature_extraction.text import CountVectorizer


def get_vectors(text1, text2):
    texts = [text1, text2]
    vectorizer = CountVectorizer()
    vectorizer.fit(texts)
    return vectorizer.transform(texts).toarray()
