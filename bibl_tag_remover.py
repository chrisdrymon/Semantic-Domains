import os
from bs4 import BeautifulSoup

folder_path = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Unannotated', 'Perseus and OGL')
os.chdir(folder_path)
indir = os.listdir(folder_path)
file_count = 1
bibl_total = 0

for file in indir:
    bibl_count = 0
    if file[-4:] == '.xml':
        print(file_count, file)
        greek_file = open(file, 'r', encoding='utf-8')
        greek_text = BeautifulSoup(greek_file, 'lxml')
        for bibl_tag in greek_text.find_all('bibl'):
            bibl_tag.decompose()
            bibl_count += 1
        file_count += 1
        print(bibl_count, 'bibliographies extracted.')
        greek_file.close()
        with open(file, 'w') as writefile:
            writefile.write(str(greek_text))
        bibl_total += bibl_count
print(bibl_total, 'bibl tags removed.')
