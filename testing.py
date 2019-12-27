from bs4 import BeautifulSoup
import re

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

#soup = BeautifulSoup(doc, 'lxml')
#soupCopy = soup
print(doc)
i = 0
bracket = 'closed'
message = ''
wordOne = ''
holdWord = 'oops'
doc2 = ''

for char in doc:
    if char == '<':
        bracket = 'open'
        doc2 = doc2 + char
    elif bracket == 'closed':
        message = message + char
        doc2 = doc2 + char
    elif char == '-' and doc[i + 1] == '\n':
        holdWord = wordOne
    elif char == ' ' or char == '\n':
        wordOne = ''
        doc2 = doc2 + char
    elif char == '>':
        bracket = 'closed'
        doc2 = doc2 + char
    else:
        wordOne = wordOne + char
        doc2 = doc2 + char
    i += 1
print(message)
print(doc2)
print(holdWord)
