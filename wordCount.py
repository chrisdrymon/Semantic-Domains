import os
from bs4 import BeautifulSoup

folderPath = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Plain Text', 'PerseusUnfolded')
os.chdir(folderPath)
indir = os.listdir(folderPath)
fileCount = 0
wordCount = 0
for file in indir:
    if file[-4:] == '.xml':
        perseusText = open(file, 'r')
        openText = BeautifulSoup(perseusText, 'lxml-xml')
        for paragraph in openText.find_all('p'):
            for word in paragraph.text.split():
                wordCount += 1
        fileCount += 1
        print(fileCount, file)

print(fileCount-1, 'files in', folderPath)
print(wordCount, 'words in corpus.')
