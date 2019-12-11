import os
from utility import deaccent
from bs4 import BeautifulSoup
from collections import Counter

folderPath = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Plain Text', 'PerseusUnfolded')
os.chdir(folderPath)
indir = os.listdir(folderPath)
fileCount = 0
wordCount = 0
wordList = Counter()
for file in indir:
    if file[-4:] == '.xml':
        print(fileCount, file)
        perseusText = open(file, 'r')
        openText = BeautifulSoup(perseusText, 'lxml-xml')
        for paragraph in openText.find_all('p'):
            i = 0
            for word in paragraph.text.split():
                if deaccent(word) == 'αντι':
                    try:
                        nextWord = paragraph.text.split()[i+1]
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
