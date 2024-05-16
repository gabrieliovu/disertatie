from googletrans import Translator

translator = Translator()
melodie = 'Coace domne prunele, sa umplem cazanele, sa curga rachiul pe teava, sa beau cu mandruta draga. Hai sa bem un paharel, numai unul mititel, hai sa bem cate-o canuta, adusa de-a mea mandruta.'

trans = translator.translate(melodie, src='ro', dest='en')

print(trans.text)