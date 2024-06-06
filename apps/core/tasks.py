import gensim.downloader as api
import nltk
from celery import Celery
from difflib import SequenceMatcher
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity

from .utils import get_vectors
from .models import TextComparison

app = Celery()


@app.task(bind=True)
def task_preprocessing(self, obj_id: int):
    obj = TextComparison.objects.get(id=obj_id)
    nltk.download('stopwords')
    nltk.download('punkt')
    text_a1 = obj.first_text
    text_a2 = obj.second_text

    # The word_tokenize() function will break our text phrases into #individual words
    tokens_text1 = sent_tokenize(text_a1)
    tokens_text2 = sent_tokenize(text_a2)

    # we'll create a new list which contains punctuation we wish to clean
    punctuations = ['(', ')', ';', ':', '[', ']', ',', '-']

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

    TextComparison.objects.filter(id=obj.id).update(
        first_text_preprocessed=phrases_text1,
        second_text_preprocessed=phrases_text2,
        first_text_tokens=tokens_text1,
        second_text_tokens=tokens_text2
    )

    task_word_vectors.delay(obj.id)
    task_sequence_matcher.delay(obj.id)
    task_get_cosine_sim.delay(obj.id)


@app.task(bind=True)
def task_word_vectors(self, obj_id: int):
    obj = TextComparison.objects.get(id=obj_id)

    phrases_text1, phrases_text2 = obj.first_text_tokens, obj.second_text_tokens

    word_vectors = api.load("glove-wiki-gigaword-300")
    identic = []
    similarity = []

    # sim = 0 means that 2 texts have exactly the same meaning
    count_sim = 0

    for i in phrases_text1:
        for j in phrases_text2:
            sim = word_vectors.wmdistance(i, j)
            if 0.6 < sim < 1:
                similarity.append([i, j])

            if sim < 0.4:
                identic.append([i, j])
            count_sim += sim

    total_checks = len(phrases_text1) * len(phrases_text2)

    obj.wmdistance.similarity = round((total_checks - count_sim) / total_checks * 100, 2)
    obj.wmdistance.similar_phrases = similarity
    obj.wmdistance.identic_phrases = identic
    obj.wmdistance.save()

    obj.overall_similarity = (int(obj.overall_similarity) + obj.wmdistance.similarity)/2
    obj.save()


@app.task(bind=True)
def task_sequence_matcher(self, obj_id: int):
    obj = TextComparison.objects.get(id=obj_id)

    phrases_text1, phrases_text2 = obj.first_text_tokens, obj.second_text_tokens
    identic = []
    similarity = []
    count_ratio = 0

    for i in phrases_text1:
        for j in phrases_text2:
            m = SequenceMatcher(None, i, j)

            # ration = 1 texts are exactly the same
            if 0.6 < m.ratio() < 0.95:
                similarity.append([i, j])
            if m.ratio() > 0.95:
                identic.append([i, j])

            count_ratio += m.ratio()

    total_checks = len(phrases_text1) * len(phrases_text2)

    obj.sequence_matcher.similarity = round((total_checks - (total_checks-count_ratio))/total_checks * 100, 2)
    obj.sequence_matcher.similar_phrases = similarity
    obj.sequence_matcher.identic_phrases = identic
    obj.sequence_matcher.save()

    obj.overall_similarity = (int(obj.overall_similarity) + obj.sequence_matcher.similarity) / 2
    obj.save()


@app.task(bind=True)
def task_get_cosine_sim(self, obj_id: int):
    obj = TextComparison.objects.get(id=obj_id)

    phrases_text1, phrases_text2 = obj.first_text, obj.second_text

    vectors = get_vectors(phrases_text1, phrases_text2)
    cosine_sim = cosine_similarity(vectors)

    obj.cosine_similarity.similarity = round(cosine_sim[0][1] * 100, 2)
    obj.cosine_similarity.save()

    obj.overall_similarity = (int(obj.overall_similarity) + obj.cosine_similarity.similarity) / 2
    obj.save()
