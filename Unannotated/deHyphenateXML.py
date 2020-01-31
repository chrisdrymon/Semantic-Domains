from utility import deaccent
import os

greekChars = ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'ς', 'τ', 'υ',
              'φ', 'χ', 'ψ', 'ω']

folderPath = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Plain Text', 'Perseus and OGL')
os.chdir(folderPath)
indir = os.listdir(folderPath)

for file in indir:
    i = 0
    bracket = 'closed'
    wordOne = ''
    doc2 = ''
    stopCharacters = [' ', '\n']
    k = 0
    ignoreHyph = 'off'
    print(file)
    docunread = open(file, 'r', encoding='utf-8')
    doc = docunread.read()
    hyphenTot = 0
    hyphenations = 0

    # If a < (less than sign) occurs, don't copy characters to the message until after a > occurs.
    # Copy every character to the new document except for the hyphenation at the end of a line.
    # After a hyphenation-new line, the following characters needs to be appended to the end of the previous word until
    # a space character.

    for char in doc:
        j = 2
        # Here to make PyCharm shut up. Assumes tags which will be looked at ahead of a hypenation are closed by
        # default.
        bTag = 'closed'
        # This keeps track of whether a tag is opened or not. The close check needs to happen toward the end of this
        # section.
        if char == '<':
            bracket = 'open'
        # This keeps track of the letters that will be the first part of the hyphenated word. It resets after every
        # space or new line.
        if char in stopCharacters:
            wordOne = ''
        else:
            wordOne = wordOne + char
        # Check if a line ends with characters + hyphen with no space between and the tag is closed.
        if bTag == 'closed' and char == '-':
            if doc[i - 1] not in stopCharacters and doc[i + 1] == '\n':
                # I can't just look for Greek here because there might be Greek within a tag. I have to make sure a tag
                # is closed.
                nextChar = doc[i + j]
                while deaccent(nextChar) not in greekChars or bTag == 'open':
                    j += 1
                    if doc[i + j] == '<':
                        bTag = 'open'
                    nextChar = doc[i + j]
                    if doc[i + j] == '>':
                        bTag = 'closed'
                addWord = ''
                k = 0
                while nextChar not in stopCharacters:
                    addWord = addWord + nextChar
                    j += 1
                    k += 1
                    nextChar = doc[i + j]
                delSpaces = len(wordOne)-1
                combinedWord = wordOne[:-1] + addWord + '\n'
                doc2 = doc2[:-delSpaces] + combinedWord
                ignoreHyph = 'on'
                hyphenations += 1
            hyphenTot = hyphenTot + hyphenations
        # Around here, doc2 = doc2[0:-4] + addWord or whatever then insert a counter to keep track of first part of
        # word.
        if k > 0 and bracket == 'closed' and deaccent(char) in greekChars:
            k -= 1
        elif ignoreHyph == 'on':
            ignoreHyph = 'off'
        else:
            doc2 = doc2 + char
        if char == '>':
            bracket = 'closed'
        i += 1
    docunread.close()
    with open(file, 'w') as writefile:
        writefile.write(str(doc2))
    print(hyphenations, 'words dehyphenated.')
