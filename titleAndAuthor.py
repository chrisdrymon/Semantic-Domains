import os
from bs4 import BeautifulSoup
import pandas as pd
from utility import deaccent
from collections import Counter

folderPath = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Plain Text',
                          'Perseus and OGL', '1.1 No Notes Index or Latin')
os.chdir(folderPath)
indir = os.listdir(folderPath)
fileCount = 1
otherCounter = Counter()
greekChars = ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'ς', 'τ', 'υ',
              'φ', 'χ', 'ψ', 'ω']
listOfLists = []
for file in indir:
    wordCount = 0
    greekWordCount = 0
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
        for paragraphs in openText.find_all('text'):
            for word in paragraphs.text.split():
                wordCount += 1
                simpleWord = deaccent(word)
                if any(letter in greekChars for letter in simpleWord):
                    greekWordCount += 1
                else:
                    otherCounter[word] += 1
        disparity = wordCount - greekWordCount
        percentOther = disparity/wordCount
        textList = [author, title, file, greekWordCount, wordCount, disparity, "{:.4f}".format(percentOther)]
        listOfLists.append(textList)
        fileCount += 1
        print(textList)
df = pd.DataFrame(listOfLists, columns=['Author', 'Title', 'File Name', 'Greek Words', 'Word Count',
                                        'Disparity', 'Percent Other'])
df.to_csv('wordcounter.csv', encoding='utf-8')
print(otherCounter)
print(fileCount-1, 'files in', folderPath)
