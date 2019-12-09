import os
from bs4 import BeautifulSoup

folderPath = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Plain Text', 'PerseusUnfolded')
os.chdir(folderPath)
indir = os.listdir(folderPath)
fileCount = 1
rootTags = []
for file in indir:
    if file[-4:] == '.xml':
        print(fileCount, file)
        perseusText = open(file, 'r')
        openText = BeautifulSoup(perseusText, 'lxml-xml')
        if openText.author:
            print(openText.author.text)
        if openText.title.text == 'Machine readable text':
            title = openText.find_all('title')[1].text
        else:
            title = openText.title.text
        print(title)
        fileCount += 1

print(fileCount-1, 'files in', folderPath)
