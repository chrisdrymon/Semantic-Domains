from utility import deaccent

greekChars = ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'ς', 'τ', 'υ',
              'φ', 'χ', 'ψ', 'ω']

doc = '''
<text>
<div n="43" subtype="chapter" type="textpart">
<p>43. Ἢν δὲ αἷμα ἐκ τόκου ἐμέσῃ, τοῦ ἥπατος θρὶξ τέτρωται,
<lb></lb>καὶ ὀδύνη πρὸς τὰ σπλάχνα φοιτᾷ, καὶ τὴν καρδίην σπᾶται. Ταύ-
την
<lb></lb>χρὴ λούειν πολλῷ θερμῷ, καὶ τῶν χλιασμάτων ἃ μάλιστα προσδέ-

<pb n="102"></pb>

χεται προστιθέναι, καὶ πιπίσκειν ὄνου γάλα ἑπτὰ ἡμέρας ἢ πέντε·
<lb></lb>μετὰ δὲ ταῦτα πιπίσκειν βοὸς μελαίνης γάλα ἄσιτον ἐοῦσαν, εἰ
<lb></lb>οἵη τε εἴη, ἡμέρας τεσσαράκοντα· ἐς δὲ τὴν ἑσπέρην σήσαμον τριπτὸν
<lb></lb>πιπίσκειν. Ἡ δὲ νοῦσος κινδυνώδης.
</p>
</div></text>
'''

print(doc)
i = 0
bracket = 'closed'
message = ''
wordOne = ''
doc2 = ''
stopCharacters = [' ', '\n']
k = 0
ignoreHyph = 'off'

# If a < (less than sign) occurs, don't copy characters to the message until after a > occurs.
# Copy every character to the new document except for the hyphenation at the end of a line.
# After a hyphenation-new line, the following characters needs to be appended to the end of the previous word until a
# space character.

for char in doc:
    j = 2
    bTag = 'closed'
    if char == '<':
        bracket = 'open'
    if bracket == 'closed':
        message = message + char
    if char == ' ' or char == '\n':
        wordOne = ''
    else:
        wordOne = wordOne + char
    # Check if a line ends with letters + hyphen with no space between
    if char == '-':
        if doc[i + 1] == '\n' and doc[i - 1] is not ' ':
            # I can't just look for Greek here because there might be Greek within a tag. I have to make sure a tag is
            # closed.
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
    # Around here, doc2 = doc2[0:-4] + addWord or whatever then insert a counter to keep track of first part of word.
    if k > 0 and bracket == 'closed' and deaccent(char) in greekChars:
        k -= 1
    elif ignoreHyph == 'on':
        ignoreHyph = 'off'
    else:
        doc2 = doc2 + char
    if char == '>':
        bracket = 'closed'
    i += 1
print("New Document\n\n")
print(doc2)
