from cltk.lemmatize.greek.backoff import BackoffGreekLemmatizer
import re

sentence = 'ἦν δὲ καὶ Σερβιλία Κάτωνος ὁμομήτριος ἀδελφή. καὶ πραγματείας παραδεχομένους· γίνεται γὰρ οἷον ἔγκαυμα. τί λέγεις; οὐχ οἷος.'

print(re.split('[·;.]', sentence))
#lemmatizer = BackoffGreekLemmatizer()

#print(lemmatizer.lemmatize(sentence)[3])
