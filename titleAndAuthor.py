import os
from bs4 import BeautifulSoup
import pandas as pd
from utility import deaccent

folderPath = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Plain Text',
                          'OpenGreekAndLatin-First1KGreek-0e92640')
os.chdir(folderPath)
indir = os.listdir(folderPath)
fileCount = 1
greekChars = ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'ς', 'τ', 'υ',
              'φ', 'χ', 'ψ', 'ω']
listOfLists = []
for file in indir:
    wordCount = 0
    if file[-4:] == '.xml':
        print(fileCount, file)
        perseusText = open(file, 'r')
        openText = BeautifulSoup(perseusText, 'lxml')
        if openText.author:
            author = openText.author.text
        else:
            author = 'Unknown'
        if openText.title.text == 'Machine readable text':
            title = openText.find_all('title')[1].text
        else:
            title = openText.title.text
        for paragraphs in openText.find_all('body'):
            for word in paragraphs.text.split():
                simpleWord = deaccent(word)
                if any(letter in greekChars for letter in simpleWord):
                    wordCount += 1
        print(author, title, wordCount)
        textList = [author, title, file, 'First1K', wordCount]
        listOfLists.append(textList)
        fileCount += 1
df = pd.DataFrame(listOfLists, columns=['Author', 'Title', 'File Name', 'Collection', 'Word Count'])
df.to_csv('first1k.csv', encoding='utf-8')
print(fileCount-1, 'files in', folderPath)
