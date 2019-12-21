from cltk.lemmatize.greek.backoff import BackoffGreekLemmatizer
import re

lemmatizer = BackoffGreekLemmatizer()

sentence = 'ἦν δὲ καὶ Σερβιλία Κάτωνος ὁμομήτριος ἀδελφή. καὶ πραγματείας παραδεχομένους· γίνεται γὰρ οἷον ἔγκαυμα. τί λέγεις; οὐχ οἷος.'
sentence = sentence.split()
#print(re.split('[·;.]', sentence))

lemmatizedSentence = lemmatizer.lemmatize(sentence)
res = [j for i, j in lemmatizedSentence]
print(res)
