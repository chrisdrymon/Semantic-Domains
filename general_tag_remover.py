import os
from bs4 import BeautifulSoup

folder_path = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Unannotated', 'Perseus and OGL')
os.chdir(folder_path)
indir = os.listdir(folder_path)
file_count = 1
tag_total = 0

for file in indir:
    tag_count = 0
    if file[-4:] == '.xml':
        print(file, file_count)
        greek_file = open(file, 'r', encoding='utf-8')
        greek_text = BeautifulSoup(greek_file, 'lxml')
        for some_tag in greek_text.find_all('interpgrp'):
            some_tag.decompose()
            tag_count += 1
        file_count += 1
        print(tag_count, 'interpreting groups extracted.')
        greek_file.close()
        with open(file, 'w') as writefile:
            writefile.write(str(greek_text))
        tag_total += tag_count
print(tag_total, 'interpreting groups removed.')
