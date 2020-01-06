from utility import deaccent

greekChars = ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'ς', 'τ', 'υ',
              'φ', 'χ', 'ψ', 'ω']

doc = '''
<text>
<div n="43" subtype="chapter" type="textpart">
<p>43. Ἢν δὲ αἷμα ἐκ τόκου ἐμέσῃ, τοῦ ἥπατος θρὶξ τέτρωται,
<lb></lb>καὶ ὀδύνη πρὸς τὰ σπλάχνα φοιτᾷ, καὶ τὴν καρδίην σπᾶται. Ταύτην
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

# If a < occurs, don't copy characters to the message until after a > occurs.
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
    if char == '-':
        if doc[i + 1] == '\n':
            # I can't just look for Greek here because there might be Greek within a tag. I have to make sure a tag is
            # closed.
            nextChar = doc[i + j]
            while deaccent(nextChar) not in greekChars or bTag == 'open':
                j += 1
                if doc[i + j] == '<':
                    bTag = 'open'
                if doc[i + j] == '>':
                    bTag = 'closed'
                nextChar = doc[i + j]
            firstChar = doc[i + j - 1]
            addWord = firstChar
            k = 1
            while nextChar is not ' ':
                addWord = addWord + nextChar
                j += 1
                k += 1
                nextChar = doc[i + j]
            combinedWord = wordOne[:-1] + addWord + '\n'
    if k > 0 and bracket == 'closed':
        k -= 1
    else:
        doc2 = doc2 + char
    if char == '>':
        bracket = 'closed'
    i += 1
print(doc2)
print(combinedWord)