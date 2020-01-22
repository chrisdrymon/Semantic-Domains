import os
from bs4 import BeautifulSoup

folder_path = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Annotated')
os.chdir(folder_path)
indir = os.listdir(folder_path)
tag_list = [[], [], [], [], [], [], [], [], [], []]
for file in indir:
    if file[-4:] == '.xml':
        print(file)
        xml_file = open(file, 'r')
        soup = BeautifulSoup(xml_file, 'xml')
        words = soup.find_all('word')
        for word in words:
            if word.has_attr('postag'):
                i = 0
                for letter in word['postag']:
                    if letter not in tag_list[i]:
                        tag_list[i].append(letter)
                    i += 1
print(tag_list)
