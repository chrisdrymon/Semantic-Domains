import os

folder_path = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Unannotated', 'Perseus and OGL',
                           'Plaintext')
os.chdir(folder_path)
indir = os.listdir(folder_path)
greek_chars = ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'ς', 'τ', 'υ',
               'φ', 'χ', 'ψ', 'ω']
file_count = 1
parentheses_total = 0
parentheses_removed_total = 0
files_changed = 0

for file in indir:
    print(file, file_count)
    unread_doc = open(file, 'r', encoding='utf-8')
    doc = unread_doc.read()
    new_doc = ''
    i = 0
    parentheses = 0
    parentheses_removed = 0
    while i < len(doc):
        if doc[i] == '(':
            j = 0
            try:
                greek = 'no'
                while doc[i+j] is not ')' and j < 70:
                    j += 1
                    if doc[i+j] in greek_chars:
                        greek = 'yes'
                    parentheses += 1
                if doc[i+j] is ')' and greek == 'no':
                    i += j
                    parentheses_removed += 1
                else:
                    new_doc += '('
            except IndexError:
                new_doc += '('
        else:
            new_doc += doc[i]
        i += 1
    with open(file, 'w') as writefile:
        writefile.write(new_doc)
    file_count += 1
    parentheses_total += parentheses
    parentheses_removed_total += parentheses_removed
    if parentheses > 0:
        files_changed += 1
    print(parentheses_removed, 'of', parentheses, 'removed.')
print(parentheses_removed_total, 'of', parentheses_total, 'removed across', files_changed, 'files.')
