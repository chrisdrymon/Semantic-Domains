import os
from utility import deaccent
from bs4 import BeautifulSoup

filePath = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Plain Text',
                        'OpenGreekAndLatin-First1KGreek-0e92640', 'tlg5023.tlg014.1st1K-grc1.xml')
wordCount = 0
perseusText = open(filePath, 'r')
openText = BeautifulSoup(perseusText, 'lxml')
greekChars = ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'ς', 'τ', 'υ',
              'φ', 'χ', 'ψ', 'ω']
for bodyText in openText.find_all('body'):
    for word in bodyText.text.split():
        simpleWord = deaccent(word)
        if any(letter in greekChars for letter in simpleWord):
            wordCount += 1
print(wordCount)
