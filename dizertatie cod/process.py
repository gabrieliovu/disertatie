
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

from nltk.tokenize import sent_tokenize, word_tokenize
a1 = open("a1.txt", "r", encoding="utf8")



text_a1 = a1.read()
#print(text_a1)
#The word_tokenize() function will break our text phrases into #individual words
tokens = sent_tokenize(text_a1)

#we'll create a new list which contains punctuation we wish to clean
punctuations = ['(',')',';',':','[',']',',','-']
#We initialize the stopwords variable which is a list of words like #"The", "I", "and", etc. that don't hold much value as keywords
stop_words = stopwords.words('english')
#We create a list comprehension which only returns a list of words #that are NOT IN stop_words and NOT IN punctuations.
phrases=[]
for i in tokens:
    words = word_tokenize(i)

    keywords = [word for word in words if not word in stop_words and not word in punctuations]
    phrases.append(' '.join(keywords))
print(phrases)