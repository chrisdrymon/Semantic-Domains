import os
from bs4 import BeautifulSoup
from bs4 import Comment

folderPath = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Plain Text', 'Perseus and OGL')
os.chdir(folderPath)
indir = os.listdir(folderPath)
fileCount = 1

for file in indir:
    commentCount = 0
    if file[-4:] == '.xml':
        print(fileCount, file)
        greekFile = open(file, 'r', encoding='utf-8')
        greekText = BeautifulSoup(greekFile, 'xml')
        comments = greekText.find_all(string=lambda text: isinstance(text, Comment))
        for c in comments:
            commentCount += 1
            c.extract()
        fileCount += 1
        print(commentCount, 'comments extracted.')
        greekFile.close()
        with open(file, 'w') as writefile:
            writefile.write(str(greekText))
print(fileCount-1, 'files in', folderPath)
