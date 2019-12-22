import os
from utility import deaccent
from bs4 import BeautifulSoup
from collections import Counter
import pandas
import re
from cltk.lemmatize.greek.backoff import BackoffGreekLemmatizer

folderPath = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Plain Text', 'Perseus and OGL',
                          '1.1 No Notes Index or Latin')
os.chdir(folderPath)
indir = os.listdir(folderPath)
fileCount = 1
wordCount = 0
wordList = Counter()
lemmatizer = BackoffGreekLemmatizer()

for file in indir:
    smallWordCount = 0
    if file[-4:] == '.xml':
        print(fileCount, file)
        perseusText = open(file, 'r')
        openText = BeautifulSoup(perseusText, 'lxml')
        for texts in openText.find_all('text'):
            splitGraph = re.split('[·;.,]', texts.text)
            for sentence in splitGraph:
                splitSentence = sentence.split()
                lemmad = lemmatizer.lemmatize(splitSentence)
                lemmaSentence = [j for i, j in lemmad]
                k = 0
                for word in lemmaSentence:
                    try:
                        nextWord = splitSentence[k+1]
                        if deaccent(word) == 'εν' and deaccent(nextWord) == 'τοις':
                            try:
                                lem3 = lemmaSentence[k+2]
                            except IndexError:
                                lem3 = 'end of clause'
                            print(word, nextWord, lem3)
                            smallWordCount += 1
                            wordCount += 1
                            wordList[deaccent(lem3)] += 1
                    except IndexError:
                        pass
                    k += 1
        fileCount += 1
        print(smallWordCount, 'εν τοις in work.')
df = pandas.DataFrame.from_dict(wordList, orient='index').reset_index()
df.to_csv('EnToisLems.csv', encoding='utf-8')
print(fileCount-1, 'files in', folderPath)
print(wordCount, 'εν τοις in corpus.')
print(wordList)
print(len(wordList), 'unique words follow εν τοις.')
