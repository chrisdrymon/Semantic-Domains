from cltk.lemmatize.greek.backoff import BackoffGreekLemmatizer

sentence = 'κατέβην χθὲς εἰς Πειραιᾶ μετὰ Γλαύκωνος τοῦ Ἀρίστωνος'.split()

lemmatizer = BackoffGreekLemmatizer()

print(lemmatizer.lemmatize(sentence)[3])
