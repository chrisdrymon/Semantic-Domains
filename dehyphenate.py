import os

folder_path = os.path.join(os.environ['HOME'], 'Google Drive', 'Greek Texts', 'Unannotated', 'Perseus and OGL',
                           'Plaintext')
os.chdir(folder_path)
indir = os.listdir(folder_path)
stop_characters = [' ', '\n']
invalid_hyphs = [' ', '\n', '-']
hyphenation_total = 0
file_count = 1

for file in indir:
    print(file_count, file)
    unread_doc = open(file, 'r', encoding='utf-8')
    doc = unread_doc.read()
    new_doc = ''
    i = 0
    hyphenation_count = 0
    while i < len(doc):
        if doc[i] == '-':
            if doc[i-1] not in invalid_hyphs and doc[i+1] == '\n':
                j = 2
                latter_part = ''
                while doc[i+j] in stop_characters:
                    j += 1
                while doc[i+j] not in stop_characters:
                    latter_part = latter_part + doc[i+j]
                    j += 1
                new_doc = new_doc + latter_part + '\n'
                i = i + j + 1
                hyphenation_count += 1
        new_doc += doc[i]
        i += 1
    with open(file, 'w') as writefile:
        writefile.write(new_doc)
    file_count += 1
    hyphenation_total += hyphenation_count
    print(hyphenation_count, 'words dehyphenated.')
print(hyphenation_total, 'words dehyphenated in all.')
