import os
from bs4 import BeautifulSoup
from utility import deaccent
import pandas

folderPath = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Plain Text', 'PerseusUnfolded',
                          'OpenGreekAndLatin-First1KGreek-0e92640', '1.1 No Notes')
os.chdir(folderPath)
indir = os.listdir(folderPath)
greekChars = ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'ς', 'τ', 'υ',
              'φ', 'χ', 'ψ', 'ω']
listOfLists = []
fileCount = 0

for file in indir:
    if file[-4:] == '.xml':
        wordCount = 0
        greekWordCount = 0
        perseusText = open(file, 'r')
        openText = BeautifulSoup(perseusText, 'lxml')
        for paragraph in openText.find_all('body'):
            for word in paragraph.text.split():
                wordCount += 1
                simpleWord = deaccent(word)
                if any(letter in greekChars for letter in simpleWord):
                    greekWordCount += 1
        fileCount += 1

        print(fileCount, file)

print(fileCount-1, 'files in', folderPath)
