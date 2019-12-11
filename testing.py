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
        perseusText = open(file, 'r')
        openText = BeautifulSoup(perseusText, 'lxml-xml')
        for paragraph in openText.find_all('p'):
            for word in paragraph.text.split():
                if word == 'ἐνδοξότερον':
                    print('Susana at', file, '.')
        perseusText.close()
