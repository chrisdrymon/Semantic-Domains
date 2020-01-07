import os
from bs4 import BeautifulSoup

folderPath = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Unannotated', 'Perseus and OGL')
savePath = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Unannotated', 'Perseus and OGL',
                        'Plaintext')
os.chdir(folderPath)
indir = os.listdir(folderPath)
fileCount = 1
greekChars = ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'ς', 'τ', 'υ',
              'φ', 'χ', 'ψ', 'ω']

for file in indir:
    os.chdir(folderPath)
    greekCount = 0
    paragraphCount = 0
    if file[-4:] == '.xml':
        print(fileCount, file)
        greekFile = open(file, 'r', encoding='utf-8')
        greekText = BeautifulSoup(greekFile, 'lxml')
        if greekText.author:
            author = greekText.author.text
        else:
            author = 'Unknown'
        if greekText.title.text == 'Machine readable text':
            title = greekText.find_all('title')[1].text
        else:
            title = greekText.title.text
        fileCount += 1
        greekFile.close()
        texts = greekText.find_all('text')
        text_file = ''
        for a_text in texts:
            text_file = text_file + a_text.text
        new_file_name = file[:-4] + '-' + author + '-' + title + '.txt'
        print(new_file_name)
        os.chdir(savePath)
        with open(new_file_name, 'w') as writefile:
            writefile.write(text_file)

print(fileCount-1, 'files in', folderPath)
