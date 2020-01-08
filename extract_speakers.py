import os
from bs4 import BeautifulSoup

folderPath = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Unannotated', 'Perseus and OGL')
os.chdir(folderPath)
indir = os.listdir(folderPath)
fileCount = 1
speakers_total = 0

for file in indir:
    print(file, fileCount)
    speaker_count = 0
    if file[-4:] == '.xml':
        print(fileCount, file)
        greekFile = open(file, 'r', encoding='utf-8')
        greekText = BeautifulSoup(greekFile, 'lxml')
        for speaker in greekText.find_all('speaker'):
            speaker.decompose()
            speaker_count += 1
        fileCount += 1
        print(speaker_count, 'speakers extracted.')
        greekFile.close()
        with open(file, 'w') as writefile:
            writefile.write(str(greekText))
    speakers_total += speaker_count
print(speakers_total, 'speakers extracted in all.')
