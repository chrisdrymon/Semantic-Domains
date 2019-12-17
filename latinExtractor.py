import os
from bs4 import BeautifulSoup
from utility import deaccent

folderPath = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Plain Text',
                          'OpenGreekAndLatin-First1KGreek-0e92640', '1.2 Removing Latin')
os.chdir(folderPath)
indir = os.listdir(folderPath)
fileCount = 1
greekChars = ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'ς', 'τ', 'υ',
              'φ', 'χ', 'ψ', 'ω']

for file in indir:
    graphCount = 0
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
        print(author, title)
        for paragraph in greekText.find_all('p'):
            simGraph = deaccent(paragraph.text)
            if any(letter in greekChars for letter in simGraph):
                pass
            else:
                paragraph.decompose()
                graphCount += 1
        fileCount += 1
        print(graphCount, 'paragraphs extracted.')
        greekFile.close()
        with open(file, 'w', encoding='utf-8') as writefile:
            writefile.write(str(greekText))

print(fileCount-1, 'files in', folderPath)
