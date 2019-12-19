import os
from utility import deaccent
from bs4 import BeautifulSoup
from collections import Counter
from cltk.lemmatize.greek.backoff import BackoffGreekLemmatizer

folderPath = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Plain Text', 'Perseus and OGL',
                          '1.1 No Notes Index or Latin')
os.chdir(folderPath)
indir = os.listdir(folderPath)
fileCount = 0
wordCount = 0
wordList = Counter()
lemmatizer = BackoffGreekLemmatizer()

for file in indir:
    if file[-4:] == '.xml':
        print(fileCount, file)
        perseusText = open(file, 'r')
        openText = BeautifulSoup(perseusText, 'lxml-xml')
        for paragraph in openText.find_all('p'):
            i = 0
            splitParagraph = paragraph.text.split()
            lemmaGraph = lemmatizer.lemmatize(splitParagraph)
            for word in splitParagraph:
                if deaccent(word) == 'αντι':
                    try:
                        # gotta fix everything from here on to match the lemmatized paragraph
                        nextWord = splitParagraph[i+1]
                    except IndexError:
                        nextWord = 'none'
                    print(word, nextWord)
                    wordCount += 1
                    wordList[deaccent(nextWord)] += 1
                i += 1
        fileCount += 1

print(fileCount-1, 'files in', folderPath)
print(wordCount, 'αντιs in corpus.')
print(wordList)
print(len(wordList), 'unique words follow αντι.')
