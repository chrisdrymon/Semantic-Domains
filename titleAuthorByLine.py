import os
from bs4 import BeautifulSoup
import pandas as pd

folderPath = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Plain Text', 'PerseusUnfolded', 'By Line')
os.chdir(folderPath)
indir = os.listdir(folderPath)
fileCount = 1
rootTags = []
listOfLists = []
for file in indir:
    wordCount = 0
    if file[-4:] == '.xml':
        print(fileCount, file)
        perseusText = open(file, 'r')
        openText = BeautifulSoup(perseusText, 'lxml-xml')
        if openText.author:
            author = openText.author.text
        else:
            author = 'Unknown'
        if openText.title.text == 'Machine readable text':
            title = openText.find_all('title')[1].text
        else:
            title = openText.title.text
        for paragraph in openText.find_all('p'):
            for word in paragraph.text.split():
                wordCount += 1
        print(author, title, wordCount)
        textList = [author, title, file, 'Perseus Unicode', wordCount]
        listOfLists.append(textList)
        fileCount += 1
df = pd.DataFrame(listOfLists, columns=['Author', 'Title', 'File Name', 'Collection', 'Word Count'])
df.to_csv('workunicode.csv', encoding='utf-8')
print(fileCount-1, 'files in', folderPath)
