import os
from bs4 import BeautifulSoup

folder_path = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Unannotated', 'Perseus and OGL')
save_path = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Unannotated', 'Perseus and OGL',
                         'Plaintext')
os.chdir(folder_path)
indir = os.listdir(folder_path)
file_count = 1

for file in indir:
    os.chdir(folder_path)
    if file[-4:] == '.xml':
        print(file_count, file)
        greek_file = open(file, 'r', encoding='utf-8')
        greek_text = BeautifulSoup(greek_file, 'xml')
        if greek_text.author:
            author = greek_text.author.text
        else:
            author = 'Unknown'
        if greek_text.title.text == 'Machine readable text':
            title = greek_text.find_all('title')[1].text
        else:
            title = greek_text.title.text
        file_count += 1
        greek_file.close()
        texts = greek_text.find_all('text')
        text_file = ''
        for a_text in texts:
            text_file += a_text.text
        new_file_name = file[:-4] + '-' + author + '-' + title + '.txt'
        print(new_file_name)
        os.chdir(save_path)
        with open(new_file_name, 'w') as writefile:
            writefile.write(text_file)
print(file_count - 1, 'files in', folder_path)
